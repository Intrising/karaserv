import json, urllib
from bottle import request, abort
import session 

def errtmpl( msg):
    return json.dumps(  { 'error': msg},  True, False, indent=4)

def oktmpl( retdic=dict()):
    return json.dumps( retdic, True, False, indent=4)

def token2user( uservar='uid'):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if 'access_token' not in request.GET:
                abort (401, 'Access Denied. You must specify access_token')
            actoken = request.GET['access_token']
            try:
                uprof = session.token2uprof( token)
            except:
                return errtmpl( 'invalid token')
            request.GET[uservar]= uid
            return func(*args, **kwargs)
        return wrapper
    return decorator

def check_token():
    def decorator(func):
        def wrapper(*args, **kwargs):
            if 'access_token' not in request.GET:
                abort (401, 'Access Denied. You must specify access_token')
            token = request.GET['access_token']
            if not session.token_valid( token):
                return errtmpl( 'invalid token')
            return func(*args, **kwargs)
        return wrapper
    return decorator

def check_params():
    def decorator(func):
        argnames=func.func_code.co_varnames[:func.func_code.co_argcount]
        if func.func_defaults:
            ndefs = len( func.func_defaults )
        else:
            ndefs = 0
        defnames = argnames[ (len(argnames)-ndefs):]
        def wrapper(*args, **kwargs):
            for argname in argnames:
                if argname in request.GET:
                    kwargs[argname]=request.GET[argname]
                else:
                    if argname not in defnames:
                        return json.dumps( {'ERROR': 'You must specify {0}'.format(argname) })
            return func(*args, **kwargs)
        return wrapper
    return decorator


