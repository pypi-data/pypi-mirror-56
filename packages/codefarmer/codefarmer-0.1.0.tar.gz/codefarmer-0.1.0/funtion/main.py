# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:59:28 2019

@author: Qiqi
"""

from .modelmix import modelaverage,modeladd
from .vote_prob import vote_prob
from .runmodelmix import main_add

def main():
    main_add()

if __name__ == '__main__':
    main()
