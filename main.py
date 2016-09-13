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
import FileSave
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
        
        self.get_filelabel=Label(master, text="Enter Get File name:")
        self.get_filelabel.pack()
        self.get_filename=Entry(master,width=20)
        self.get_filename.pack()        
        
        self.out_filelabel=Label(master, text="Enter Destination File name:")
        self.out_filelabel.pack()
        self.out_filename=Entry(master,width=20)
        self.out_filename.pack()        
        
        self.encrypt = Button(master, text="File Put", fg="black", command=self.file_put, width=25,height=5);
        self.encrypt.pack(side=LEFT)
        self.decrypt = Button(master,text="File Get", fg="black",command=self.file_get, width=25,height=5)
        self.decrypt.pack(side=RIGHT)
    
    # empty password alert
    def pass_alert(self):
        tkMessageBox.showinfo("Password Alert","Please enter a password.")
    
    def get_file_alert(self):
        tkMessageBox.showinfo("Get File Alert","Please enter a complete file name.")
    
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
            ConvergentEncrypt.dedup_convergent_encrypt_file(in_filename=str(in_filename),user_key=user_key)
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
            out_file=None
            if(self.out_filename.get()==""):
                out_file=None
            else:
                out_file=self.out_filename.get();
            
            ConvergentEncrypt.dedup_convergent_decrypt_file(in_filename=in_filename,out_filename=out_file,user_key=user_key)
     
    def file_put(self):
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
            #ConvergentEncrypt.dedup_convergent_encrypt_file(in_filename=str(in_filename),user_key=user_key)
            FileSave.FilePut(in_filename,user_key,chunksize=64*1024);            
            self.enc_success(in_filename)
        print"\n\n\n"
    def file_get(self):
        self.file_path_d=None
    
        dec_pass = self.passg.get()
        if dec_pass == "":
            self.pass_alert()
        else:    
            user_key = hashlib.sha256(dec_pass).digest()
            get_filename = self.get_filename.get()
            
            self.file_path_d = os.path.dirname(get_filename)
            # decrypt the ciphertext
            out_file=None
            if(self.out_filename.get()==""):
                out_file=None
            else:
                out_file=self.out_filename.get();
            
            FileSave.FileGet(get_filename,out_file,user_key,chunksize=64*1024)
        print"\n\n\n"


root = Tk()
root.wm_title("Image Encryption")
app = App(root)
root.mainloop()