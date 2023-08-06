# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:25:18 2019

@author: Qiqi
"""

import os
from setuptools import setup, find_packages


#path = os.path.abspath(os.path.dirname(__file__))
#
#try:
#  with open(os.path.join(path, 'README.md')) as f:
#    long_description = f.read()
#except Exception as e:
#  long_description = "customize okta cli"

setup(
    name = "codefarmer",
    version = "1.1.0",
#    keywords = ("pip", "okta", "cli", "cmd", "steven"),
    description = "ccf contest",
    long_description = 'This is the code packages of little codefarmer team',
#    long_description_content_type='text/markdown',
    python_requires=">=3.5.0",
    license = "we are the champion",

#    url = "https://github.com/stevenQiang/okta-cmd",
    author = "cyq",
    author_email = "596871173@qq.com",

    packages = find_packages(),
    include_package_data = True,
    install_requires = ['pandas','numpy'],
    platforms = "any",

#    scripts = [],
#    entry_points = {
#        'console_scripts': [
#            'okta-cmd=oktacmd:main_cli'
#        ]
#    }
)