# kar3a-jwt
Python3 JWT Authentication Plugin for bottle.py applications.

This module is inspired from <a href="https://github.com/agile4you/bottle-jwt/">Agile4you's bottle-jwt</a>.
I have ported it for Python3 (tested with Python3.5).
Fixed encoding problems when b64 enconding (Python3 specific).
I have abstracted and isolated the authentication method so any method could be plugged in (see authentication.py).
I have also done minimal disambiguation of exceptions handling.
The claims part of the token still provides base64 encoded values. This very well might not be RFC compliant.
The generated token is valid if tested with <a href="https://jwt.io/">Auth0's jwt.io</a>  with the right HMAC secret.
Still needs to be PEP8 proofed, don't have the time as of right now.
Suggestions are welcome as issues in this github repo.
-mak