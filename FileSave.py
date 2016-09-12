# -*- coding: utf-8 -*-
"""
Created on Tue Sep 06 12:52:16 2016

@author: CrySPUser2
"""

import shelve
import ConvergentEncrypt
import HashFile

def FilePut(in_filename,user_key="123456",chunksize=64*1024):
    d=shelve.open('testshelf.db')
    hashed_filename=HashFile.hash_file()
    
    
    
    
    
def FileGet(filename,user_key="123456"):
    print "hi"