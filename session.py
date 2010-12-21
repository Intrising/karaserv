import urllib,urllib2
import json
import time
from userdb import *

def queryuser_facebook( token):
    fburl='https://graph.facebook.com/me?access_token={0}'.format(token)
    af=urllib.urlopen( fburl)
    udic=json.load(af)
    return udic

#TODO: support more social networks
def scnet_query( token):
    sctoken, scnet= token.split( '@')
    if scnet=='fb':
        try:
            udic = queryuser_facebook(sctoken)
        except:
            raise Exception( 'invalid token')
    else:
        raise Exception( 'no such social network:'+scnet)
    #TODO: design a abstract class to unify user profile from 
    #every social network
    udic['uid']='{0}/{1}'.format( scnet, udic['id'])
    return udic

def token_format_valid( token):
    try:
        token, scnet = token.split( '@')
        if (scnet!='fb') | (len(token)<5):
            return False
    except ValueError:
        return False
    return True

sesstbl=dict()
def session_new( token, uprof):
    #check member ship & permission
    sesstbl[token] = { 'login_since': time.time(), 'profile':uprof}
    return sesstbl[token]

def session_list():
    import pprint
    pprint.pprint( sesstbl)

    
#there are many cases upon the login procedure
def login( token):
    if not token_format_valid( token):
        raise Exception('incorrect token format ')
    #check if he has been logged in, or not
    try:
        sess = sesstbl[token]
    except KeyError:
        pass

    #if not, let's query his basic profile throught his social network
    user_scprof = scnet_query( token)
    #if nothing found, there must be something wrong in his token
    if user_scprof == None:
        raise Exception('invalid token')
   
    #we got his basic profile, let's check if he has been registered
    user_prof = userdb_query( user_scprof['uid'])
    #if not, register for him first
    if user_prof == None:
        user_prof = userdb_register( user_scprof)

    #create a new session for him
    return session_new( token, user_prof)

def logout( token):
    try:
        sess = sesstbl.pop(token)
        profile=sess['profile']
        timetup = (sess['login_since'], time.time())
        logmsg = '{0}~{1}'.format( time.ctime(sess['login_since']), time.ctime())
        print '{0} logged out.  {1}'.format( profile['name'], logmsg)
        profile['logons'].append( timetup)
        userdb_set( profile['uid'], profile)
    except KeyError:
        pass
    userdb_save()

if __name__ == '__main__':
    def load_actoken():
        fbtoken = open('/tmp/fbtokens.txt').read().strip('\r\n')
        fbtoken = urllib.unquote(fbtoken)
        return '{0}@{1}'.format( fbtoken,'fb')

    def test1():
        actoken = load_actoken()
        sess = login( actoken)
        session_list()
        logout(actoken)
        userdb_dump()
    test1()
