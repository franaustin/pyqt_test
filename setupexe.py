# -*- coding: utf-8 -*-
'''
Created on 2013-8-28
@author: chex
@subject: py2exe生成exe文件
'''
from distutils.core import setup
import py2exe
import sys

reload(sys) 
sys.setdefaultencoding('utf-8') 
#setup(windows=[{"script":"main.py"}], options={"py2exe":{"includes":["sip"]}})
includes = ["encodings", "encodings.*","sip"]    

if len(sys.argv) == 1:
    sys.argv.append("py2exe")
    
options = {"py2exe":
    {"compressed": 1, 
     "optimize": 1,
     "ascii": 1,
     "includes":includes,
     "bundle_files": 1 
    }
    }           
setup(
    version = "1.0.0.0001",
    name = "Tetris",      
    options = options,      
    zipfile = None, 
    description = "A application. With development of Python",
    windows =[{"script": "tetris.py","icon_resources": [(1, "arithmetic.ico")]}]  #
    #windows =[{"script": "spider_qiushibaike.py","icon_resources": [(1, "pick4ab.ico")]}] 
    )

