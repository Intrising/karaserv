import json,urllib
from bottle import route, run, template, request, response, error,debug
import songdb


def simplify_singers( se):
    se['singer'] = '&'.join( se['singer'])

def add_mvurl(se):
    se['mvurl']= 'http://175.41.182.66:8080/getmv?v={0}'.format(se['mvfn'])

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
