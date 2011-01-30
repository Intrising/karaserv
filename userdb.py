import time
import shelve

#def userdb_init():
guserdb = shelve.open( 'users.db') 

def userdb_query( uid):
    if uid in guserdb:
        return guserdb[ uid]

def userdb_register( user_scprof):
    uid = user_scprof['uid']
    #user profile is firstly stolen from his social network
    user_prof = user_scprof.copy()
    #then add our own specific stuff
    user_prof['register_date'] = time.time()
    user_prof['playlist']= []
    user_prof['play_history']=[]
    user_prof['paid_date']=[]
    user_prof['logons']=[]
    guserdb[uid] = user_prof
    return guserdb[uid]

def userdb_set( uid, user_prof):
    guserdb[uid]=user_prof

def userdb_dump():
    import pprint
    pprint.pprint( guserdb)

def userdb_getall():
    return dict(guserdb)

def userdb_save():
    guserdb.sync()

