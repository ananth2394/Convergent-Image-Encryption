# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 02:27:04 2016

@author: Ananth Narayan
"""
import hashlib
def hash_file(in_filename,hasher=hashlib.md5(),chunksize=64*1024):
    """
        Hashes contents of file in_filename using the md5 secure hash and returns the hexdigest
    """
    print "File hashed: " + in_filename
    with open(in_filename,'rb') as infile:
        buf = infile.read(chunksize);
        while len(buf)>0:
            hasher.update(buf);
            buf=infile.read(chunksize);
        infile.close()
    
    return hasher.digest(),hasher.hexdigest()
        