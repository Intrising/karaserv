import json,urllib
from bottle import route, run, template, request, response, error, redirect,debug
import songdb


def simplify_singers( se):
    se['singer'] = '&'.join( se['singer'])

def add_mvurl(se):
    if se['mvfn']:
        se['mvurl']='http://kemity.game-server.cc:8080/getmv?v={0}'.format(se['mvfn'])
    else:
        se['mvurl']=''

def fix_song_entry( se):
    newse = se.copy()
    simplify_singers( newse)
    add_mvurl( newse)
    return newse
   

@route('/qsong', method='GET')
def qsong():
    print 'querystring=', request.query_string
    for f in songdb.songdb.fieldnames:
        qval = request.GET.get( f , '').strip()
        if qval:
            break
    if qval==None:
        #raise HTTPError(code=403)
        return 'Error: no such field'
    qval=urllib.unquote(qval)
    ses = systemdb.query( qval, field=f)
    if len(ses)==0:
        return 'Error: not found' 
        #raise HTTPError(code=403)
    newses = [ fix_song_entry(se) for se in ses]
    return json.dumps( newses, True, False, indent=4)

@route('/qsinger', method='GET')
def qsinger():
    for f in ['lang', 'gender']:
        qval = request.GET.get( f , '').strip()
        if qval:
            break
    singers = systemdb.qsingers( f, qval)
    if len(singers)==0:
        return 'Error: not found' 
        #raise HTTPError(code=403)
    return json.dumps( singers, True, False, indent=4)

@route('/search', method='GET')
def searchsong():
    for f in ['name', 'singer', 'any']:
        qval = request.GET.get( f , '').strip()
        if qval:
            break
    if qval==None:
        return "invalid query"
    ses = systemdb.search( qval, field=f)
    if len(ses)==0:
        return "couldn't find any song matched"
    newses = [ fix_song_entry(se) for se in ses]
    return json.dumps( newses, True, False, indent=4)


import session
from common_response import errtmpl, oktmpl, check_params,check_token

@route('/login')
@check_params()
def login( access_token):
    try:
        ret = session.login( access_token) 
    except Exception as e:
        return errtmpl( '{0}:{1}'.format( type(e), e))
    return oktmpl(ret )

@route('/logout')
@check_params()
def logout( access_token):
    try:
        session.logout( access_token)
    except Exception as e:
        return errtmpl( '{0}:{1}'.format( type(e), e))
    return oktmpl()

@route('/plins')
@check_token()
@check_params()
def playlist_insert( access_token, sno, pos=0):
    session.playlist_insert( access_token, sno, pos)
    return oktmpl('')

@route('/pldel')
@check_token()
@check_params()
def playlist_delete( access_token, pos=999):
    session.playlist_delete( access_token, pos) 
    return oktmpl()

@route('/plset')
@check_token()
@check_params()
def playlist_set( access_token):
    return oktmpl('')

@route('/plget')
@check_token()
@check_params()
def playlist_get( access_token ):
    snolist= session.playlist_get( access_token) 
    return oktmpl( {'playlist': snolist})


@route('/listusers')
def listusers():
    pass

import awsutils
@route('/getmv')
@check_params()
def getmv(v, fmt='orig'):
    vurl = awsutils.aws_get_mvurl( v,fmt)
    if vurl:    
        return redirect(vurl)
    else:    
        return errtmpl( 'no such mv')

@route('/getau')
@check_params()
def getau( a ):
    aurl = awsutils.aws_get_auurl( a)
    if aurl:
        return redirect( aurl)
    else:
        return errtmpl( 'no such audio')

@route('/mytable')
def createtab():
    output = template('make_table', rows=['i', 'dont',  'care'])
    return output

import sys,songdb
import ConfigParser

systemdb = songdb.songdb( sys.argv[1] )
config = ConfigParser.RawConfigParser()
config.read('karaserv.cfg')
debug(True)
host=config.get('network', 'host')
port=config.getint('network', 'port')

run( host=host,  port=port)
