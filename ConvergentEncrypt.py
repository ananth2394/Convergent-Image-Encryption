
import EncryptFile
import hashlib
import os
import binascii
import HashFile
import shelve

shelfname = "tempshelf.db"
keyshelfname = "keyshelf.db"

def convergent_encrypt_file(in_filename,out_filename=None,key_filename=None,user_key="123456",chunksize=64*1024):
    """
        convergently encrypts file in_filename
        
        user_key is derived from password given by user. It is used to encrypt the key
    """
    # get directory names and create new file and key names, filename stored as in_filename.enc. key stored in in_filename.key    
    cur_dir = os.getcwd()
    basic_file_name = os.path.basename(in_filename)    
    
    new_file_path = cur_dir+"\\encrypted_files"
    new_key_path = cur_dir + "\\encryption_keys"
    
    if(out_filename==None):
        new_file_name = os.path.join(new_file_path,basic_file_name+'.enc') ;
        new_key_name = os.path.join(new_key_path,basic_file_name+'.key');
    else:
        if(key_filename==None):
            key_filename=out_filename
            
        new_file_name = os.path.join(new_file_path,out_filename+'.enc') ;
        new_key_name = os.path.join(new_key_path,key_filename+'.key');
    
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
    EncryptFile.encrypt_file(hashlib.sha256(user_key).digest(),tmp_key_path,new_key_name,chunksize)
    os.remove(tmp_key_path)
    
def convergent_decrypt_file(in_filename,out_filename=None,key_filename=None,user_key="123456",chunksize=64*1024):
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
   
    if(out_filename==None):
        new_file_name = os.path.join(new_file_path,os.path.splitext(basic_filename)[0]+".bin") ;
        if(key_filename==None):
            key_filename=os.path.splitext(basic_filename)[0]
    else:
        new_file_name = os.path.join(new_file_path,out_filename) ;
        if key_filename == None:
            key_filename = out_filename
        
    print "Destination file name: "+ new_file_name
    #new_key_name = os.path.join(new_key_path,os.path.splitext(basic_filename)[0]+".key") ;
    
        
    new_key_name=os.path.join(new_key_path,key_filename+".key")
    
    print "New file name:" + new_file_name
    print "New key name:" + new_key_name    
    # create decrypted_files directory
    if not os.path.exists(new_file_path):
        os.makedirs(new_file_path)
    #deccrypt key file
    
    EncryptFile.decrypt_file(hashlib.sha256(user_key).digest(),new_key_name,"tmp.key",chunksize)
   
    with open("tmp.key",'rb') as infile:
        generated_key=infile.read(chunksize)
        infile.close()
        
    #decrypt main file
    os.remove("tmp.key")    
    EncryptFile.decrypt_file(generated_key,in_filename,new_file_name,chunksize)
    
def dedup_convergent_encrypt_file(in_filename,user_key="123456",chunksize=64*1024):
    
    d = shelve.open(shelfname)
    encrypted_file_name = None    
    try:    
        encrypted_file_name = str(d[str(in_filename)])
        print "We are here with " + in_filename
        print "d[in_filename]: "+ encrypted_file_name
    except KeyError:
        print "Caught!"
        encrypted_file_name = None
    finally:
        d.close()
        
    if not(encrypted_file_name==None):
        #file already encrypted before probably
        if os.path.exists(os.getcwd()+ "\\encrypted_files\\" + encrypted_file_name+".enc"):
            print "File exists. No need to encrypt"
            return
        else:
            basic_filename = os.path.basename(encrypted_file_name)
            print "Basic filename: " + basic_filename
            print "Without ext: " + os.path.splitext(basic_filename)[0]
            h = hashlib.sha256(encrypted_file_name)
            h.update(user_key)
            key_filename = str(h.hexdigest())
            convergent_encrypt_file(in_filename,os.path.splitext(basic_filename)[0],key_filename,user_key,chunksize)
    
    else:
        convergent_encrypt_file(in_filename,"tmp","tmp",user_key,chunksize)
        cur_dir = os.getcwd()
        out_filename = str(HashFile.hash_file(cur_dir+"\\encrypted_files\\"+"tmp.enc",hashlib.sha256(),chunksize)[1])
        out_filename=str(hashlib.sha256(out_filename).hexdigest())   
        
        h = hashlib.sha256(out_filename)
        h.update(user_key)
        key_filename = str(h.hexdigest()) 
        
        os.rename(cur_dir+"\\encrypted_files\\"+"tmp.enc",cur_dir+"\\encrypted_files\\"+out_filename+".enc") 
        os.rename(cur_dir+"\\encryption_keys\\"+"tmp.key",cur_dir+"\\encryption_keys\\"+key_filename+".key")
        
        d = shelve.open(shelfname)
        try:    
            print "We are here with " + in_filename
            d[str(in_filename)]=str(out_filename)
            print "d[in_filename]: "+d[str(in_filename)]
        except:
            print "COuld not store!"
        finally:
            d.close()
        
        #convergent_encrypt_file(in_filename,out_filename,user_key,chunksize)

def dedup_convergent_decrypt_file(in_filename,out_filename=None,user_key="123456",chunksize=64*1024):
    basic_filename = os.path.basename(in_filename)
    file_without_ext = os.path.splitext(basic_filename)[0]
   
    h = hashlib.sha256(file_without_ext)
    h.update(user_key)
    key_filename = str(h.hexdigest())
    
    
    convergent_decrypt_file(in_filename,out_filename,key_filename,user_key,chunksize)
        
        
    
    
        
    