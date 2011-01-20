from bottle import route, run, redirect, debug
from common_response import errtmpl, oktmpl, check_params,check_token
import boto                                                                     
from boto.s3.key import Key

def aws_connect():
    import ConfigParser
    config = ConfigParser.RawConfigParser()
    config.read('aws.cfg')
    access_key=config.get('Credentials', 'access_key')
    secret_key=config.get('Credentials', 'secret_key')
    return boto.connect_s3( access_key, secret_key)

@route('/getmv')
@check_params()
def getmv(v, fmt='orig'):
    k = mvbkt.get_key('mvsong/{0}/{1}.mp4'.format( fmt, v));
    rurl = k.generate_url( 60)
    return redirect(rurl)


s3conn= aws_connect()
mvbkt = s3conn.get_bucket('mdsmv')

debug(True)
run(host='10.128.54.121', port=8081)
