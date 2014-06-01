#!/usr/bin/env python
import re

class functions():
    
    @staticmethod
    #Check if the user uses an aiesec account
    def auth_user(user):
        #email_rexp = re.compile(r'^[_A-Za-z0-9-\\+]+(\\.[_A-Za-z0-9-]+)*@unis.edu.gt')
        email_rexp = re.compile(r'^[_A-Za-z0-9-\\+]+(\\.[_A-Za-z0-9-]+)*@gmail.com')
        return email_rexp.match(user)
    
    @staticmethod
    def permission_user(user):
        user_dict = {'renatoreyesdeleon@gmail.com':'A1','jperezlopez18@gmail.com':'SUSAC'}
        return (user_dict.get(user.email()) if user_dict.get(user.email()) is not None else '-')