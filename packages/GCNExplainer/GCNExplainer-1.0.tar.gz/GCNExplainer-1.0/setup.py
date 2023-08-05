# -*- coding: utf-8 -*-
# @Time    : 2019-11-18 09:26
# @Author  : Jason
# @FileName: setup.py

from setuptools import setup
from setuptools import find_packages

setup(name="GCNExplainer",
      version="1.0",
      description="Explain the complex model, you can show most important edges by using this model",
      author="Zhang Pin",
      author_email="zhangpin@geetest.com",
      install_requires=["keras", "numpy", "pandas", "scipy", "matplotlib", "networkx"],
      url="https://geetest.com",
      download_url="https://pypi.org/manage/project/gnnexplainer/releases/",
      packages=find_packages())
