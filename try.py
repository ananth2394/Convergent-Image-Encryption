# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 17:14:12 2016

@author: CrySPUser2
"""

import ConvergentEncrypt

in_filename = raw_input("Filename?: ")
user_key = raw_input("User key?: ")

ConvergentEncrypt.dedup_convergent_encrypt_file(in_filename,user_key,chunksize=64*1024);

