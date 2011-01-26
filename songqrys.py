import intlmsgs
class qrybase:
	datas=[]
	def items( self):
		return self.datas
	def query( self, itemth):
		return self.func( self.datas[itemth])

class qry_singer(qrybase):
    def __init__(self):
		self.datas = [ 'male', 'female', 'band']
    def func( self, d):
        return { 'rtype':'singer', 'rdata':['blah']}
			
class qry_bopomofo( qrybase):
    def __init__(self):
        bpmf=intlmsgs.gettext('bopomofo_list')
        self.datas = [ ch for ch in bpmf]
    def func( self, d):
		return { 'rtype':'song', 'rdata':['blah']}

class qry_chinese(qrybase):
    def __init__(self):
        self.datas = [ str(nch)+' chars' for nch in xrange(1,11)]
    def func( self, d):
		return { 'rtype':'song', 'rdata':['blah']}

class qry_alpha(qrybase):
    def __init__(self):
        self.datas = [chr(i) for i in xrange(ord('a'), ord('z')+1)]
    def func( self, d):
		return { 'rtype':'song', 'rdata':['blah']}

class qry_taiwanese(qrybase):
    def __init__(self):
        self.datas = [ str(nch)+' chars' for nch in xrange(1,11)]
    def func( self, d):
   		return { 'rtype':'song', 'rdata':['blah']}

class qry_english(qrybase):
    def __init__(self):
        self.datas = [ str(nch)+' words' for nch in xrange(1,11)]
    def func( self, d):
   		return { 'rtype':'song', 'rdata':['blah']}


if __name__ == '__main__':
	qry = qry_singer()
	d = qry.items()
	print d
	qry.query(1)
	qry.func( 'ff')
