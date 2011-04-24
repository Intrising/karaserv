import boto
from boto.s3.key import Key

def aws_connect():
    import ConfigParser
    config = ConfigParser.RawConfigParser()
    config.read('aws.cfg')
    access_key=config.get('Credentials', 'access_key')
    secret_key=config.get('Credentials', 'secret_key')
    return boto.connect_s3( access_key, secret_key)

"""
def aws_get_mvurl( v, fmt='orig'):
    k = songbkt.get_key('mvsong/{0}/{1}.mp4'.format( fmt, v))
    if k:
        return k.generate_url( 60)

def aws_get_midiurl( a):
    fn='{0}.mm3'.format(a)
    k = songbkt.get_key('midisong/'+fn)
    if k:
        return k.generate_url( 60)

def aws_get_auurl( a, lyric):
    if lyric>0:
        fn='{0}.js'.format(a)
    else:
        fn='{0}.mp3'.format(a)
    k = songbkt.get_key('ausong/'+fn)
    if k:
        return k.generate_url( 60)

def aws_get_bgurl( v, fmt='orig'):
    k = songbkt.get_key('bgvideo/{0}/{1}.mp4'.format( fmt, v))
    if k:
        return k.generate_url( 60)
"""

cfdist='d1eca33vh79jq5.cloudfront.net'
def aws_get_mvurl( v, fmt='orig'):
    fn = 'mvsong/{0}/{1}.mp4'.format( fmt, v)
    return 'https://{0}/{1}'.format( cfdist, fn)

def aws_get_midiurl( a):
    fn='midisong/{0}.mm3'.format(a)
    return 'https://{0}/{1}'.format( cfdist, fn)

def aws_get_auurl( a, lyric):
    if lyric>0:
        fn='{0}.js'.format(a)
    else:
        fn='{0}.mp3'.format(a)
    ffn = 'ausong/{0}'.format(fn)
    return 'https://{0}/{1}'.format( cfdist, ffn)

def aws_get_bgurl( v, fmt='orig'):
    fn ='bgvideo/{0}/{1}.mp4'.format( fmt, v)
    return 'https://{0}/{1}'.format( cfdist, fn)

def aws_get_bgvlist():
    bgvkeys = [ k for k in songbkt.list('bgvideo/orig') if k.name.endswith('.mp4')]
    bgdics=[]
    for k in bgvkeys:
        v = k.name.split( '/')[-1].split('.')[0]
        bgname='BG{0}'.format(v)
        md5str= k.etag.strip('"').decode('utf-8')
        bgdic = { 'v':v, 'name':bgname, 'url': aws_get_bgurl(v), 'size': k.size,  'md5sum':md5str }
        bgdics.append( bgdic)
    return bgdics

def aws_close():
    songbkt.close()
    s3conn.close()

s3conn= aws_connect()
songbkt = s3conn.get_bucket('mdsmv')

