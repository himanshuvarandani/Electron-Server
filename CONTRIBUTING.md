# Contributing

Please follow these sections for frequent use-cases in the application.


### Securing an endpoint
To make sure an endpoint is accessed by a trusted origin, we need to configure
`fastapi-jwt-auth` for that endpoint like so -

```python
from fastapi import Depends
from fastapi_jwt_auth import AuthJWT


@app.get('/protected')
def protected(Auth: AuthJWT = Depends()):
    Auth.jwt_required()
    # Rest of the code...
```

> `Auth`should be the last argument if the view function has multiple arguments (i.e.body, params or headers).
