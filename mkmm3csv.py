import os,sys,glob
import subprocess
from songdb import systemdb

def collect_mm_info(ffn):
    cmd='./iytmf_info -s skey_mm3.bin -b {0}'.format( ffn)
    pobj =subprocess.Popen( cmd, stdout=subprocess.PIPE, shell=True)
    return pobj.stdout.read().strip('\r\n')

def ensure_readable( s):
    sno = int( s.split('\t')[0])
    return sno, s.decode('utf-8')

def append_photourl(sno, us):
    songs = systemdb.query(sno)
    photourl=''
    if len(songs)>0:
        song = songs[0]
        if len(song['photourl'])>0:
            photourl=song['photourl']
    return '{0}\t{1}\t{2}'.format( us.encode('utf-8'), photourl, sno)


mmdir = sys.argv[1]
mmffns = glob.glob( '{0}/*.mm3'.format(mmdir))
for mmffn in mmffns:
    csvline = collect_mm_info(mmffn)
    try:
        sno,ustr=ensure_readable(csvline)
    except:
        sys.stderr.write('cannot read {0}\n'.format(csvline))
        continue
    csvline = append_photourl( sno,ustr)
    print csvline
