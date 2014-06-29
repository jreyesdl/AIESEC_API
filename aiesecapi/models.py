from google.appengine.api import memcache
from google.appengine.ext import endpoints
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from endpoints_proto_datastore.ndb import EndpointsModel

import logging

class University(EndpointsModel):
    univ_id = ndb.StringProperty(required = True)
    name = ndb.StringProperty(required = True)
    
    @staticmethod
    def get_uById(univ_id):
        key = 'Univ'
        universities = memcache.get(key)
    
class User(EndpointsModel):
    user_id = ndb.StringProperty(required = True)
    email = ndb.StringProperty()
    user  = ndb.StringProperty()
    university = ndb.StringProperty()
    state = ndb.BooleanProperty()
    
    @staticmethod
    def get_user(update = False):
        key = 'user'
        users = memcache.get(key)
        user_key = ndb.Key('AIESEC','User')
           
        if users is None or update:
            users = ndb.gql("SELECT user_id FROM User WHERE ANCESTOR IS :1", user_key)
            users = list(users)
            memcache.set(key,users)
            
        results = [x[1].user_id for x in enumerate(users)]
        return results
    
    @staticmethod
    def get_userById(user_id):
        key = 'user_list'
        users = memcache.get(key)
        user_key = ndb.Key('AIESEC','User')
         
        if users is None:
            users = ndb.gql("SELECT * FROM User WHERE ANCESTOR IS :1", user_key)
            logging.debug('Usuarios:%s'%users)
            users = list(users)
            memcache.set(key,users)
          
        result = [x[1] for x in enumerate(users) if x[1].user_id == user_id]
        logging.debug(result)
        return result

class Post(EndpointsModel):
    title = ndb.StringProperty(required=True)
    date  = ndb.DateTimeProperty(auto_now_add=True)
    text  = ndb.TextProperty()
    blob_key = ndb.BlobKeyProperty()
    blob_url = ndb.StringProperty()
    owner = ndb.StructuredProperty(User)
    status = ndb.BooleanProperty(default=True)
    eID = ndb.StringProperty(default="")#Property for getting the response
    image = ndb.BlobProperty()#Property for getting the response
    
    @staticmethod
    def list_(update = False):
        key = 'post_list'
        posts = memcache.get(key)
        post_key = ndb.Key('AIESEC','Post')
           
        if posts is None or update:
            posts = ndb.gql("SELECT * FROM Post WHERE ANCESTOR IS :1", post_key)
            posts = list(posts)
            memcache.set(key,posts)
    
        return posts
    
class Comment(EndpointsModel):
    text = ndb.StringProperty()
    post = ndb.StructuredProperty(Post)