from protorpc import messages


class LoginResponse(messages.Message):
    signedIn = messages.BooleanField(1,required = True)
    
class PermissionResponse(messages.Message):
    permission = messages.StringField(1,required = True)
    
class EmaiRequest(messages.Message):
    email = messages.StringField(1, required = True)
    
class PostRequest(messages.Message):
    key = messages.StringField(1)
 
class TokenRequest(messages.Message):
    PageToken = messages.StringField(1)

class PostResponse(messages.Message):
    title = messages.StringField(1)
    text = messages.StringField(2)
    ownerEmail = messages.StringField(3)
    ownerNickName = messages.StringField(4)
    image = messages.StringField(5)
    date = messages.StringField(6)
    key = messages.StringField(7)
   
class TimelineResponse(messages.Message):
    items = messages.MessageField(PostResponse, 1, repeated=True)
    next = messages.StringField(2)

class CommentResponse(messages.Message):
    text = messages.StringField(1)
    date = messages.StringField(2)
    owner = messages.StringField(3)

class CommentListResponse(messages.Message):
    items = messages.MessageField(CommentResponse, 1, repeated=True)
    next = messages.StringField(2)

class PostIDrequest(messages.Message):
    postID = messages.StringField(1)
    PageToken = messages.StringField(2)