# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 13:21:07 2016

@author: Ananth Narayan
"""
from Tkinter import *
from tkFileDialog import *
import tkMessageBox
import ConvergentEncrypt
import hashlib
import os
class App:
    def __init__(self,master):
        
        #front end titles
        title = "Image Encryption"
        author = "Ananth Narayan/ananth360@gmail.com"
        msgtitle = Message(master, text =title)
        msgtitle.config(font=('helvetica', 17, 'bold'), width=200)
        msgauthor = Message(master, text=author)
        msgauthor.config(font=('helvetica',10), width=200)
        
        # draw canvas
        canvas_width = 200
        canvas_height = 50
        w = Canvas(master, width=canvas_width,height=canvas_height)
        
        
        # pack the GUI, this is basic, we shold use a grid system
        msgtitle.pack()
        msgauthor.pack()
        w.pack()
        
        # password field here above buttons
        passlabel = Label(master, text="Enter Encrypt/Decrypt Password:")
        passlabel.pack()
        self.passg = Entry(master, show="*", width=20)
        self.passg.pack()
        
        self.encrypt = Button(master, text="Convergent Encrypt", fg="black", command=self.file_open, width=25,height=5);
        self.encrypt.pack(side=LEFT)
        self.decrypt = Button(master,text="Convergent Decrypt", fg="black",command=self.cipher_open, width=25,height=5)
        self.decrypt.pack(side=RIGHT)
    
    # empty password alert
    def pass_alert(self):
        tkMessageBox.showinfo("Password Alert","Please enter a password.")
   
    def enc_success(self,imagename):
        tkMessageBox.showinfo("Success","Encrypted Image: " + imagename)
        
    def file_open(self):
        self.file_path_e=None
    
        # check to see if password entry is null.  if yes, alert
        enc_pass = self.passg.get()
        if enc_pass == "":
            self.pass_alert()
        else:
            user_key = hashlib.sha256(enc_pass).digest()
            in_filename = askopenfilename()
            print "File: " +  in_filename
            self.file_path_e = os.path.dirname(in_filename)
            ConvergentEncrypt.convergent_encrypt_file(in_filename,user_key)
            self.enc_success(in_filename)
    def cipher_open(self):
        self.file_path_d=None
    
        dec_pass = self.passg.get()
        if dec_pass == "":
            self.pass_alert()
        else:    
            user_key = hashlib.sha256(dec_pass).digest()
            in_filename = askopenfilename()
            self.file_path_d = os.path.dirname(in_filename)
            # decrypt the ciphertext
            ConvergentEncrypt.convergent_decrypt_file(in_filename,user_key)
            



root = Tk()
root.wm_title("Image Encryption")
app = App(root)
root.mainloop()