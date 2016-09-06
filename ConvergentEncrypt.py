
import EncryptFile
import hashlib
import os
import binascii
import HashFile
def convergent_encrypt_file(in_filename,user_key,chunksize=64*1024):
    """
        convergently encrypts file in_filename
        
        user_key is derived from password given by user. It is used to encrypt the key
    """
    # get directory names and create new file and key names, filename stored as in_filename.enc. key stored in in_filename.key    
    cur_dir = os.getcwd()
    basic_file_name = os.path.basename(in_filename)    
    
    new_file_path = cur_dir+"\\encrypted_files"
    new_key_path = cur_dir + "\\encryption_keys"
    
    new_file_name = os.path.join(new_file_path,basic_file_name+'.enc') ;
    new_key_name = os.path.join(new_key_path,basic_file_name+'.key');
    
    generated_key = HashFile.hash_file(in_filename,hashlib.sha256())[0]
    tmp_key_path = "tmp.key"
    
    with open(tmp_key_path,'wb') as outfile:
        outfile.write(generated_key)
        outfile.close()
    
    
    
    
    #create directories if they don't exist already
    if not os.path.exists(new_file_path):
        os.makedirs(new_file_path)
    if not os.path.exists(new_key_path):
        os.makedirs(new_key_path)
        
    #Write encrypted file
    EncryptFile.encrypt_file(generated_key,in_filename,new_file_name,chunksize)
    
    #Write encrypted key and delete tmp.key file
    EncryptFile.encrypt_file(user_key,tmp_key_path,new_key_name,chunksize)
    os.remove(tmp_key_path)
    
def convergent_decrypt_file(in_filename,user_key,chunksize=64*1024):
    """
    convergently decrypts in_filename
    """
    
    # get directory names and create new file and key names, filename stored as in_filename.enc. key stored in in_filename.key    
    cur_dir = os.getcwd()
    basic_filename = os.path.basename(in_filename)
  
    print basic_filename
    print os.path.splitext(basic_filename)
      
    new_file_path = cur_dir+"\\decrypted_files"
    new_key_path = cur_dir + "\\encryption_keys"    
    
    new_file_name = os.path.join(new_file_path,os.path.splitext(basic_filename)[0]) ;
        
    new_key_name = os.path.join(new_key_path,os.path.splitext(basic_filename)[0]+".key") ;
    
    
    # create decrypted_files directory
    if not os.path.exists(new_file_path):
        os.makedirs(new_file_path)
    #deccrypt key file
    
    EncryptFile.decrypt_file(user_key,new_key_name,"tmp.key",chunksize)
   
    with open("tmp.key",'rb') as infile:
        generated_key=infile.read(chunksize)
        infile.close()
        
    #decrypt main file
    os.remove("tmp.key")    
    EncryptFile.decrypt_file(generated_key,in_filename,new_file_name,chunksize)