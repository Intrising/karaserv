import json,urllib
from bottle import route, run, template, request, response, error,debug
import songdb


def simplify_singers( ses):
    for se in ses:
        newsinger = '&'.join(se['singer'])
        se['singer']=newsinger

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
    simplify_singers(ses)
    return json.dumps( ses, True, False, indent=4)

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
    for f in ['name', 'singer']:
        qval = request.GET.get( f , '').strip()
        if qval:
            break
    if qval==None:
        return "invalid query"
    ses = systemdb.search( qval, field=f)
    if len(ses)==0:
        return "couldn't find any song matched"
    simplify_singers( ses)
    return json.dumps( ses, True, False, indent=4)


@route('/mytable')
def createtab():
    output = template('make_table', rows=['i', 'dont',  'care'])
    return output

import sys,songdb
systemdb = songdb.songdb( sys.argv[1] )
debug(True)
run(  port=8080)
