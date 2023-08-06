from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="zlapp",
    version="2.8.0",
    author="lanmengfei",
    author_email="865377886@qq.com",
    description="兰孟飞深圳市筑龙科技的工作",
    long_description=open("README.rst",encoding="utf8").read(),
    url="https://github.com/lanmengfei/testdm",
     packages=find_packages(),
     #package_data={"lmfgg.ps":['*.txt'],"lmfgg.getdata":['*.txt']},
    install_requires=[
        "pandas >= 0.13",
        "lmf>=2.1.2",
        "psycopg2-binary",
        "requests",
        "lxml",
        "pycryptodome",
        "wget"
        ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5"
    ],
)


#python  setup.py sdist &  twine upload dist/* & rd /s /q dist & rd /s /q zlapp.egg-info & python -m pip install zlapp==2.7.7