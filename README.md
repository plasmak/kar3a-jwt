# kar3a-jwt
<h1>Python3 JWT Authentication Plugin for bottle.py applications.</h1>

<p>This module is inspired from <a href="https://github.com/agile4you/bottle-jwt/">Agile4you's bottle-jwt</a>.</p>
<ul> What's different :
    <li>I have ported it for Python3 (tested with Python3.5).</li>
    <li>Fixed encoding problems when b64 enconding (Python3 specific).</li>
    <li>I have abstracted and isolated the authentication method so any method could be plugged in (see authentication.py).</li>
    <li>I have also done minimal disambiguation of exceptions handling.</li>
    <li>The claims part of the token still provides base64 encoded values. This very well might not be RFC compliant.</li>
    <li>The generated token is valid if tested with <a href="https://jwt.io/">Auth0's jwt.io</a>  with the right HMAC secret.</li>
    <li>Still needs to be PEP8 proofed, don't have the time as of right now.</li>
    <li>Suggestions are welcome as issues in this github repo.</li>
</ul>
<p>Just in case you mind: kar3a means "bottle" in arabic ;)/p>
<b>-mak</b>
