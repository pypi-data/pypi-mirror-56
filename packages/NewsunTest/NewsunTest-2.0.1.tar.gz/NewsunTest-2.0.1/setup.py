from __future__ import print_function
from setuptools import setup, find_packages
import NewsunTest

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="NewsunTest",
    version="2.0.1",
    author="Newsun",
    author_email="546331893@qq.com",
    description="my pip test",
    long_description="dont know",
    long_description_content_type="text/markdown",
    license="MIT",
    url="http://www.baidu.com",
    packages=find_packages(),
    install_requires=[

        ],
    classifiers=[
        "Topic :: Games/Entertainment ",
        'Topic :: Games/Entertainment :: Puzzle Games',
        'Topic :: Games/Entertainment :: Board Games',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
