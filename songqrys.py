import intlmsgs
from songdb import systemdb

def shrink_range( rlist, selrange):
    l = len(rlist)
    lb, ub=selrange
    return rlist[lb:ub]

class qrybase:
    datas=[]
    def items( self):
        return self.datas
    def query( self, d, qrange=(0,20)):
        if isinstance( d, str):
            allr = self.func( int(d))
        else:
            allr = self.func(d)
        subr= { 'rtype':allr['rtype'], 'rdata':[]}
        lb,ub=qrange
        for rd in allr['rdata'][lb:ub]:
            if subr['rtype']=='song':
                newse = rd.copy()
                newse['singer'] = '&'.join( newse['singer'])
                rd=newse
            subr['rdata'].append(rd)
        return subr

class qry_singer(qrybase):
    def __init__(self):
        self.datas = [ 'male', 'female']
    def func( self, d):
        gs=['M', 'F']
        singers = systemdb.qsingers( 'gender', gs[d])
        return { 'rtype':'singer', 'rdata':singers}
            
class qry_bopomofo( qrybase):
    def __init__(self):
        bpmf=intlmsgs.gettext('bopomofo_list')
        self.datas = [ ch for ch in bpmf]
    def func( self, d):
        return { 'rtype':'song', 'rdata':[]}

class qry_alpha(qrybase):
    def __init__(self):
        self.datas = [chr(i) for i in xrange(ord('a'), ord('z')+1)]
    def func( self, d):
        songs = systemdb.mquery( { 'lang':3, 'nwords': d+1})
        return { 'rtype':'song', 'rdata':songs}


class qry_chinese(qrybase):
    def __init__(self):
        self.datas = [ str(nch)+' chars' for nch in xrange(1,11)]
    def func( self, d):
        songs = systemdb.mquery( { 'lang':1, 'nwords': d+1})
        return { 'rtype':'song', 'rdata':songs}

class qry_taiwanese(qrybase):
    def __init__(self):
        self.datas = [ str(nch)+' chars' for nch in xrange(1,11)]
    def func( self, d):
        songs = systemdb.mquery( { 'lang':2, 'nwords': d+1})
        return { 'rtype':'song', 'rdata':songs}

class qry_english(qrybase):
    def __init__(self):
        self.datas = [ 'all']
    def func( self, d):
        songs = systemdb.mquery( { 'lang':3 })
        return { 'rtype':'song', 'rdata':songs}

class qry_japanese(qrybase):
    def __init__(self):
        self.datas = [ 'all']
    def func( self, d):
        songs = systemdb.mquery( { 'lang':4})
        return { 'rtype':'song', 'rdata':songs}

class qry_cantonese(qrybase):
    def __init__(self):
        self.datas = [ str(nch)+' chars' for nch in xrange(1,11)]
    def func( self, d):
        songs = systemdb.mquery( { 'lang':5, 'nwords': d+1})
        return { 'rtype':'song', 'rdata':songs}

class qry_children(qrybase):
    def __init__(self):
        self.datas = ['all']
    def func( self, d):
        songs = systemdb.mquery( { 'lang':6})
        return { 'rtype':'song', 'rdata':songs}

if __name__ == '__main__':
    qry = qry_singer()
    d = qry.items()
    print d
    print qry.query( 1)
