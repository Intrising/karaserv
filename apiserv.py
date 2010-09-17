import json,urllib
from bottle import route, run, template, request, response, error,debug
import songdb

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
    return json.dumps( ses, True, False, indent=4)

@route('/qsinger', method='GET')
def qsinger():
	
@route('/grepsong', method='GET')
def grepsong():
    for f in ['name', 'singer']:
        qval = request.GET.get( f , '').strip()
        if qval:
            break
    if qval==None:
        return "invalid query"
    ses = systemdb.grep( qval, field=f)
    if len(ses)==0:
        return "couldn't find any song matched"
    return json.dumps( ses, True, False, indent=4)


@route('/mytable')
def createtab():
    output = template('make_table', rows=['i', 'dont',  'care'])
    return output

import sys,songdb
systemdb = songdb.songdb( sys.argv[1] )
debug(True)
run( host='kemity.game-server.cc', port=8080)
