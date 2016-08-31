import bottle
import base64
import collections
import jwt
import datetime

class JWTReplier:
    def auth_succeeded(self, token_string):
        return {"token": token_string}

    def auth_failed(self, arguments):
        bottle.abort(403, '{"Error": "' + arguments + '"}')

    def auth_required(self, arguments):
        bottle.abort(401, '{"Error": "' + arguments + '"}')

class JWTProvider:
    def __init__(self, abstract_authentication, secret, algorithm='HS256', ttl=None):
        self.abstract_authentication = abstract_authentication
        self.secret = secret
        self.algorithm = algorithm
        self.ttl = ttl

    def expires(self):
        return datetime.datetime.utcnow() + datetime.timedelta(seconds=self.ttl)

    def create_token(self, user):
        payload = {self.abstract_authentication.abstract_fields.user_id: 
                        base64.b64encode(user.encode()).decode('utf-8')}
        if self.ttl:
            payload['exp'] = self.expires

        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def validate_token(self, token=''):
        if not token:
            raise JWTProviderError('No JWT token received')

        try:
            decoded = jwt.decode(
                token.split(" ", 1).pop(),
                self.secret,
                algorithms=self.algorithm
            )

            user_uid = decoded.get(self.abstract_authentication.abstract_fields.user_id)

            if not user_uid:
                raise JWTProviderError('no user id received')

            # Token validation should only be dependant on the signature here.
            # Any checks related to the User objects model (if user exists for example)
            # should not be done here as it would inject unecessary dependency in this
            # jwt class.
            return decoded

        except jwt.DecodeError as de:
            raise JWTProviderError('decoding failed')

        except jwt.ExpiredSignatureError as ese:
            raise JWTProviderError('expired signature')

    def authenticate(self, request):
        try:
            return self.create_token(self.abstract_authentication.authenticate(request))
        except ValueError as ve:
            raise JWTProviderError(str(ve))       

    def authorize(self, request):
        user_token = request.get_header("Authorization", '')
        return self.validate_token(user_token) or False


class JWTBottlePlugin:
    scope = ('plugin', 'middleware')
    api = 2

    def __init__(self, keyword, auth_endpoint, login_enable=True,
                 scope='plugin', replier=JWTReplier(), **kwargs):
        self.keyword = keyword
        self.login_enable = login_enable
        self.scope = scope
        self.provider = JWTProvider(**kwargs)
        self.auth_endpoint = auth_endpoint
        self.replier = replier

    def setup(self, app):

        if self.login_enable:
            @app.post(self.auth_endpoint)
            def auth_handler():
                try:
                    token = self.provider.authenticate(bottle.request)
                    return self.replier.auth_succeeded(token.decode("utf-8"))

                except ValueError as ve:
                    return self.replier.auth_failed(str(ve))

        for other in app.plugins:
            if not isinstance(other, JWTBottlePlugin):
                continue
            if other.keyword == self.keyword:
                raise bottle.PluginError("Found another plugin with conflicting "
                                         "settings (non-unique keyword).")

    def apply(self, callback, context):
        def wrapper(*args, **kwargs):
            try:
                self.provider.authorize(bottle.request)
                return callback(*args, **kwargs)

            except JWTProviderError as jwtpe:
                return self.replier.auth_failed(str(jwtpe))

        if self.scope == 'middleware':
            return wrapper

        if not hasattr(callback, 'auth_required'):
            return callback

        return wrapper

    
# Actual decorator to add before routes
def require_jwt_auth(callable_obj):
    setattr(callable_obj, 'auth_required', True)
    return callable_obj


class JWTProviderError(Exception):
    pass

