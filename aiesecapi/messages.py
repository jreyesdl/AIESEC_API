from protorpc import messages


class LoginResponse(messages.Message):
    signedIn = messages.BooleanField(1,required = True)
    
class PermissionResponse(messages.Message):
    permission = messages.StringField(1,required = True)
    
class EmaiRequest(messages.Message):
    email = messages.StringField(1, required = True)
    
    
    
    
