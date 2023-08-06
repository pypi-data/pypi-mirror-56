from distutils.core import setup
from setuptools import  find_packages

import os

def get_readme():
  from os import path
  this_directory = path.abspath(path.dirname(__file__))
  with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
      long_description = f.read()
  return long_description


envs = os.environ

version = envs.get("version", "0.0.15")
url = envs.get("url", "https://git.slock.it/in3/c/in3-python/")
download_url = envs.get("download_url","https://git.slock.it/in3/c/in3-python/-/archive/dev_0.1.0/in3-python-dev_0.1.0.tar.gz")
license = envs.get("license", "MIT")
description = envs.get("description", "In3 client for python")
keywords = envs.get("keywords", "in3,in3py").split(",")

name = envs.get("name", "in3")
author = envs.get("author", "Slockit")
author_email = envs.get("author_email", "developer@slock.it")
classifiers = envs.get("classifiers", "Development Status :: 3 - Alpha, Intended Audience :: Developers, Programming Language :: Python :: 3 ").split(",")


setup(
  name = name,
  # packages = find_packages(),
  packages = ["in3py"],
  include_package_data=True,
  version = version,
  license=license,
  description = description,
  author = author,
  author_email=author_email,
  url = url,
  # download_url=download_url,
  keywords = keywords,
  install_requires=[],
  classifiers=classifiers,
  long_description=get_readme(),
  long_description_content_type='text/markdown'
)

# 'Development Status :: 3 - Alpha',
# 'Intended Audience :: Developers',
# 'Topic :: Software Development :: Build Tools',
# 'License :: OSI Approved :: MIT License',
# 'Programming Language :: Python :: 3',
# 'Programming Language :: Python :: 3.4',
# 'Programming Language :: Python :: 3.5',
# 'Programming Language :: Python :: 3.6',