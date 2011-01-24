import boto                                                                     
from boto.s3.key import Key

def aws_connect():
    import ConfigParser
    config = ConfigParser.RawConfigParser()
    config.read('aws.cfg')
    access_key=config.get('Credentials', 'access_key')
    secret_key=config.get('Credentials', 'secret_key')
    return boto.connect_s3( access_key, secret_key)

def aws_get_mvurl( v, fmt):
    k = mvbkt.get_key('mvsong/{0}/{1}.mp4'.format( fmt, v))
    if k:
        return k.generate_url( 60)

def aws_get_auurl( a, lyric):
    if lyric>0:
        fn='{0}.js'.format(a)
    else:
        fn='{0}.mp3'.format(a)
    k = mvbkt.get_key('ausong/'+fn)
    if k:
        return k.generate_url( 60)

def aws_close():
    mvbkt.close()
    s3conn.close()

s3conn= aws_connect()
mvbkt = s3conn.get_bucket('mdsmv')

