from collections import namedtuple
from bottle import request

auth_fields = namedtuple('abstract_fields', ['user_id', 'user_secret'])

class AbstractAuthentication:
    
    def __init__(self, input_fields_names, auth_method):  
        self.abstract_fields = auth_fields(*input_fields_names)
        self.abstract_auth_method = auth_method

    def authenticate(self, request):
        if request.content_type.startswith('application/json'):
            credentials = request.json
        else:
            credentials = request.forms

        try:
            user_id = credentials[self.abstract_fields.user_id]
            user_secret = credentials[self.abstract_fields.user_secret]

            if self.abstract_auth_method(user_id, user_secret):
                return user_id

            raise ValueError('Login failed')
        
        except KeyError: 
            raise ValueError('Login or password missing')



 



    

 
  