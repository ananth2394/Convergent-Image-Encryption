# -*- coding: utf-8 -*-
"""
Created on Tue Sep 06 12:52:16 2016

@author: CrySPUser2
"""

import shelve
import ConvergentEncrypt
import HashFile
import os

shelfname = "tempshelf.db"
keyshelfname = "keyshelf.db"
ext_shelf = "ext_shelf.db"

def FilePut(in_filename,user_key="123456",chunksize=64*1024):
    ConvergentEncrypt.dedup_convergent_encrypt_file(in_filename,user_key,chunksize=64*1024)
    
    
    
    
    
def FileGet(get_filename,out_filename=None,user_key="123456",chunksize=64*1024):
    d=shelve.open(shelfname)
    print "\n\nFilename to be gotten:" + get_filename
    try:
        in_filename=d[str(get_filename)]
        print "get_filename" + get_filename
        print "in_filename: " + in_filename
    except KeyError:
        print "File doesn't exist!"
        in_filename=None        
        return
    finally:
        d.close()
    
    base_filename = os.path.basename(get_filename)
    ext = os.path.splitext(base_filename)[1]
    
    if out_filename == None:
        out_filename = os.path.splitext(base_filename)[0]
        
    
    full_filename = os.getcwd()+"\\encrypted_files\\"+in_filename+".enc"
    ConvergentEncrypt.dedup_convergent_decrypt_file(full_filename,out_filename+ext,user_key,chunksize)
    
    