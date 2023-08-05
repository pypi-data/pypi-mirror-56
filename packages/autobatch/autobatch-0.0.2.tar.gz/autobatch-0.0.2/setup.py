import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autobatch",
    version="0.0.2",
    author="kaijien xue",
    author_email="chuang_xue@qq.com",
    description="auto batch process ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kaijien/autobatch",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)