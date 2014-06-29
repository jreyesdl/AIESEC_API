#!/usr/bin/env python
import re
from google.appengine.api import files
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class functions():
    
    @staticmethod
    #Check if the user uses an aiesec account
    def auth_user(user):
        #email_rexp = re.compile(r'^[_A-Za-z0-9-\\+]+(\\.[_A-Za-z0-9-]+)*@aiesec.net')
        email_rexp = re.compile(r'^[_A-Za-z0-9-\\+]+(\\.[_A-Za-z0-9-]+)*@gmail.com')
        return email_rexp.match(user)
    
    @staticmethod
    def permission_user(user):
        user_dict = {'renatoreyesdeleon@gmail.com':'A1','jperezlopez18@gmail.com':'SUSAC'}
        return (user_dict.get(user.email()) if user_dict.get(user.email()) is not None else '-')
    

class uploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    
    @staticmethod
    def uploadImage(b64image):
        file_name = files.blobstore.create(mime_type='image/png')
        
        with files.open(file_name, 'a') as f:
            f.write(b64image)
            
        files.finalize(file_name)
        
        key = files.blobstore.get_blob_key(file_name)
        
        return key