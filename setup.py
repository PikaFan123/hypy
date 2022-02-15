import os
from setuptools import setup


def read(fname):
    """read... file"""
    # https://pythonhosted.org/an_example_pypi_project/setuptools.html
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="hypy-hypixel",
    version="1.4.0",
    description="A Hypixel API Wrapper",
    url="https://github.com/PikaFan123/hypy",
    author="PikaFan123",
    license="MIT License",
    long_description=read("readme.rst"),
    packages=["hypy", "hypy.ext", "hypy.ext.collisions", "hypy.ext.senither", "hypy.ext.skyhelper"],
    install_requires=["aiohttp", "dataclasses", "aiofiles", "nbt", "orjson"],
    python_requires=">=3.8,<4.0",
)
