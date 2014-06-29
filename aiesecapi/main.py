from google.appengine.ext import endpoints
from google.appengine.ext import ndb
from google.appengine.api import memcache
from protorpc import message_types
from protorpc import remote

from google.appengine.api.images import get_serving_url
from endpoints_proto_datastore.ndb import EndpointsModel

#Messages for login With AIESEC.net
from messages import LoginResponse

#Messages for users' permissions
from messages import PermissionResponse
from messages import EmaiRequest
from messages import PostRequest
from messages import PostResponse
from messages import TimelineResponse

#Global functions
from models import User 
from models import Post
from models import Comment
from models import University

from functions import functions
from functions import uploadHandler

import logging
import json
import base64

#Clients IDs
WEB_CLIENT_ID = '701424510160-upb8hkmvcem4kg7dgqi14a144q7ted5e.apps.googleusercontent.com'
EMAIL_SCOPE = 'https://www.googleapis.com/auth/userinfo.email'

@endpoints.api(name='userAPI',version='v1',
               allowed_client_ids=[WEB_CLIENT_ID,endpoints.API_EXPLORER_CLIENT_ID],
               scopes = [EMAIL_SCOPE],
               description='API for AIESEC users.')
class UserApi(remote.Service):

    @University.method(user_required = True,
                       http_method = 'POST',
                       name = 'University.insert',
                       path = 'university')
    def insert_university(self,university):
        pass
    
    @User.method(http_method = 'POST',
                 name ='user.insert',
                 path ='user')   
    def insert_user(self, _user):
        if (functions.auth_user(_user.email)):
            user_key = ndb.Key('AIESEC','User')
            u = User.get_user()
                    
            if _user.user_id in u:
                raise endpoints.InternalServerErrorException()
            else:
                user = User(parent = user_key, user_id = _user.user_id,
                            email = _user.email, user = _user.user,
                            university = _user.university, state = _user.state)
                user.put()
                User.get_user(True)
                return _user
        else:
            raise endpoints.UnauthorizedException('This method requires you to be authenticated. You may need to activate the toggle above to authorize your request using OAuth 2.0.')

    #INSERT POST METHOD
    @Post.method(http_method = 'POST',
                 name = 'post.insert',
                 path = 'post')
    def post_insert(self, _post):
        owner = User.get_userById(_post.owner.user_id)
        post_key = ndb.Key('AIESEC','Post')
        user_key = ndb.Key('AIESEC', 'User')
        
        if owner:
            
            key = uploadHandler.uploadImage(_post.image)
            url = get_serving_url(key)
            
            post_ = Post(parent = post_key, title = _post.title,
                     text = _post.text, blob_key = key, blob_url = url,
                     owner = User(parent = user_key,user_id = owner[0].user_id, email = owner[0].email, user = owner[0].user,
                                  university = owner[0].university, state = owner[0].state)
                      )
            post_.put()
            Post.list_(True)
            entityKey = str(post_.key.id())
            _post.eID = entityKey
            return _post
        else:
            raise endpoints.InternalServerErrorException()
    
    #LIST ALL THE POST        
    @endpoints.method(message_types.VoidMessage,TimelineResponse,
                      name = 'post.timeline2',
                      path = 'post/timeline',
                      http_method='GET')
    def post_timeline(self,unused_request):
        post = []
        posts = Post.list_()
        p = [x[1] for x in enumerate(posts)]
        for p in p:
            logging.debug('Post %s' %p)
            post.append(PostResponse(title=p.title,text=p.text,ownerEmail = p.owner.email, ownerNickName = p.owner.user,
                                image=p.blob_url))

        return TimelineResponse(items = post)
    
    #GET A POST BY ITS ID 
    @endpoints.method(PostRequest,PostResponse,
                 http_method = 'POST',
                 name = 'post.getById',
                 path = 'post/getById')
    def post_getById(self,request):
        logging.debug('Key: %s' %request.key)
        posts = Post.list_()
        p = [x[1] for x in enumerate(posts) if str(x[1].key.id()) == request.key]
        logging.debug('Post: %s' %p)
        if p:
            return PostResponse(title=p[0].title,text=p[0].text,ownerEmail = p[0].owner.email, ownerNickName = p[0].owner.user,
                                image=p[0].blob_url)
        else:
            return PostResponse()
        
    #METHOD FOR INSERT COMMENTS
    @Comment.method(http_method = 'POST',
                 name = 'comment.insert',
                 path = 'comment')
    def comment_insert():
        pass
    
    #SIGNIN METHOD
    @endpoints.method(EmaiRequest,LoginResponse,
                 path = 'login',
                 name = 'user.login',
                 http_method = 'POST')
    def singin_user(self,request):
        current_user = request.email
        if current_user is None:
            raise endpoints.UnauthorizedException('No user is logged in.')
    
        if (functions.auth_user(current_user)):
            return (LoginResponse(signedIn = True))
        else:
            raise endpoints.UnauthorizedException('Ivalid token.')
    
    #CHECK PERMISSIONS
    @endpoints.method(EmaiRequest,PermissionResponse,
                      path = 'permission',
                      name = 'user.permission',
                      http_method = 'GET')
    def permission_user(self,request):
        current_user = request.email
        if current_user is None:
            raise  endpoints.UnauthorizedException('Invalid token.')
        
        if (functions.auth_user(current_user)):
            return PermissionResponse(permission = functions.permission_user(current_user))
        else:
            raise endpoints.UnauthorizedException('Invalid token.')
        
application = endpoints.api_server([UserApi])