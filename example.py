import bottle
from kar3a import JWTBottlePlugin
from kar3a import AbstractAuthentication
from kar3a import require_jwt_auth

# I assume that the HTML input tag in the login form are named "login" and 
# password respectively. You could choose whatever you want (see namedtuple 
# implementation in kar3a-jwt.py inspired from bottle-jwt)

# In bottle-jwt, authentication is handled in the FakeBackend class which
# is (imho) useless. I have abstracted authentication (see authentication.py)
def trivial_auth(login, password):
    if login == 'test' and password == 'test': 
        return True
    return False

auth_method = AbstractAuthentication(('login', 'password'), trivial_auth)
server_secret = '@#$!@&^%&@^$&'

#  create a example app
app = bottle.Bottle()

# Install plugin (I encourage you to read Bottle's plugin dev doc' especially 
# about how plugin installation works and how decorators are applied)
app.install(
    JWTBottlePlugin(
        keyword='jwt',
        auth_endpoint='/jwt',
        abstract_authentication=auth_method,
        secret=server_secret
    )
)

# set example route requiring a valid token
@app.post('/')
@require_jwt_auth
def private_resource():
    return "Request accepted!"


# Demo server
bottle.run(
    app=app,
    host='0.0.0.0',
    port=8081, 
    debug=True
)