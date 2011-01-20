import boto                                                                     
from boto.s3.key import Key

def aws_connect():
    import ConfigParser
    config = ConfigParser.RawConfigParser()
    config.read('aws.cfg')
    access_key=config.get('Credentials', 'access_key')
    secret_key=config.get('Credentials', 'secret_key')
    return boto.connect_s3( access_key, secret_key)

def aws_init():
    s3conn= aws_connect()
    mvbkt = s3conn.get_bucket('mdsmv')

def aws_get_mvurl( fn, fmt):
    k = mvbkt.get_key('mvsong/{0}/{1}.mp4'.format( fmt, v));
    return k.generate_url( 60)
 
def aws_close():
    mvbkt.close()
    s3conn.close()
