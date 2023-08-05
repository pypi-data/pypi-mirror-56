import time
from threading import Thread, Event
from queue import Queue
import uuid 
class AutoBatch: 
    def __init__(self, logger = None, debug = False):
        if logger == None:
            from loguru import logger         
        self.logger = logger
        self.func = {}
        self.debug = debug
        
    def batch_process(self, batch_size, timeout = 120):
        def _batch_ptocess(func):
            def wrapper(*args):
                try:
                    if len(args) == 2:
                        cls_, data_list = args
                    else:
                        data_list = args
                        cls_ = None
                    if func.__name__ not in self.func.keys():
                        if self.debug:
                            self.logger.info('this func is not config, build...')
                        self.build_woker(func, batch_size, cls_)                        
                    message_id = uuid.uuid1().hex

                    ## config the event for get return data
                    event= Event()
                    event_condition = len(data_list) # a count for event ,when event_condition == 0,all data is processed 

                    ## 
                    self.func[func.__name__]['return_buffer'][message_id] = [None for _ in range(len(data_list))]

                    self.func[func.__name__]['events'][message_id] = {'event':event,"condition":event_condition}
                    for index, a_data in enumerate(data_list):
                        self.func[func.__name__]['send_queue'].put(((message_id,index), a_data))
                    event.wait(timeout)
                    return self.func[func.__name__]['return_buffer'].pop(message_id)
                except Exception as e:
                    print(e)
                    return -1
            return wrapper
        return _batch_ptocess
    def build_woker(self, func, batch_size,func_cls):
        '''
        build worker thread and queue
        '''
        
        self.func[func.__name__] = {}
        self.func[func.__name__]['send_queue'] = Queue()
        self.func[func.__name__]['return_buffer'] = {}
        self.func[func.__name__]['thread'] = Thread(target=self.get_batch_and_process, args=[func, batch_size], daemon=True)
        self.func[func.__name__]['events'] = {}
        self.func[func.__name__]['thread'].start()
        self.func[func.__name__]['func_cls'] = func_cls
        return True
    def get_batch_and_process(self,func, batch_size):
        while True:
            data_list = []
            message_id_list = []
            message_id_index, a_data = self.func[func.__name__]['send_queue'].get()
            data_list.append(a_data)
            message_id_list.append(message_id_index)
            while not self.func[func.__name__]['send_queue'].empty() and len(data_list) < batch_size:
                message_id_index, a_data = self.func[func.__name__]['send_queue'].get()
                data_list.append(a_data)
                message_id_list.append(message_id_index)
            if self.func[func.__name__]['func_cls'] == None:
                result_list = func(data_list)
            else:
                result_list = func(self.func[func.__name__]['func_cls'], data_list)
            
            for iter_ in range(len(message_id_list)):
                if message_id_list[iter_][0] in self.func[func.__name__]['return_buffer'].keys():
                    self.func[func.__name__]['return_buffer'][message_id_list[iter_][0]][message_id_list[iter_][1]] = result_list[iter_]
                    self.func[func.__name__]['events'][message_id_list[iter_][0]]["condition"] -= 1
                    if self.func[func.__name__]['events'][message_id_list[iter_][0]]["condition"] == 0:
                        self.logger.info(f'the {message_id_list[iter_][0]} is done, send return event')
                        self.func[func.__name__]['events'][message_id_list[iter_][0]]['event'].set()
                else:
                    self.logger.warning(f'not {message_id_list[iter_][0]} in {func.__name__} return_buffer')
