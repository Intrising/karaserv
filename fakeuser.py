import os,sys
import shelve
import pprint
from songdb import systemdb


def list_users( udb):
    udic=dict(udb)
    pprint.pprint( udic)

def addto_playlist( udb, scuid, nwords):
    songs = systemdb.mquery( {'nwords':nwords, 'stype':'mv'})
    snolist=[s['sno'] for s in songs[:10]]
    # a shelve db can't deliberately update like a dict, we need to
    # convert it to a dict and update by shelve.update()
    udic=dict(udb)
    udic[scuid]['playlist']=snolist
    udb.update( udic)

    print 'add {0} to user {1}'.format( snolist, scuid)
    udb.sync()

if __name__ == '__main__':
    userdb = shelve.open(sys.argv[1])
    while True:
        c=raw_input("choose what to do:")
        if c=='q':
            break
        elif c=='l':    
            list_users( userdb)
        elif c=='a':    
            addto_playlist(userdb, 'fb/602368881', 10)
            addto_playlist(userdb, 'fb/1537421953', 6)
            #addto_playlist(userdb, 0, 6)
        elif c=='d':    
            del userdb['qq']
    userdb.close()
