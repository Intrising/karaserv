import intlmsgs
import songqrys
from OrderedDict import OrderedDict

intlmsgs.initpo()
_ = intlmsgs.gettext

def qry2menu( qry):
	return OrderedDict([( d, qry.query) for d in qry.items()])
	

menu_top = OrderedDict([
    ( 'language', OrderedDict ([
        ('chinese', qry2menu( songqrys.qry_chinese())), 
        ('taiwanese', qry2menu( songqrys.qry_taiwanese())),
        ('english', qry2menu( songqrys.qry_english())),
        ('japanese', qry2menu( songqrys.qry_japanese())),
        ('cantonese', qry2menu( songqrys.qry_cantonese())),
        ('children', qry2menu( songqrys.qry_children())),
    ])),
    ( 'singer', qry2menu( songqrys.qry_singer())),
    ( 'phosym', OrderedDict([
        ('bopomofo', qry2menu( songqrys.qry_bopomofo())),
        ('alpha', qry2menu( songqrys.qry_alpha()))
	]))
])

def dump_menu(m, prefix=''):
    for k,v in m.items():
        chch=''
        if isinstance( v, dict):
            chch= ':'
        print '{0}{1}{2}'.format( prefix, _(k).encode('utf-8'), chch)
        if isinstance( v, dict):
            dump_menu( v, prefix+'\t')

def mkmaddr( maddr, nd):
	if maddr:
		naddr = list(maddr)
		naddr.append(str(nd))
	else:
		naddr = str(nd)
	return '_'.join( naddr)
	
def run_menu(  maddr=[]):
	m = menu_top
	title = 'topmenu'
	for d in maddr:
		title,v = m.items()[int(d)]
		m = v
	if isinstance( m, dict):
		alist=[]
		for i,k in enumerate(m.keys()):
			arec = { 'qid': mkmaddr( maddr, i), 'caption': _(k).encode( 'utf-8')}
			alist.append( arec)
		retdic= { 'rtype':'submenu', 'rdata': alist}	
	else:
		retdic= m( maddr[-1])
	retdic[ 'title'] = _(title).encode('utf-8')
	return retdic

if __name__ == '__main__':
	dump_menu( menu_top)
	qds=[]
	while True:
		nm=run_menu( qds )
		print 'title: {0}'.format( nm['title'])
		print nm['rtype']
		print nm['rdata'] 			

		c=raw_input("Pick a number between 0-{0}:".format( len( nm['rdata'])-1))
		if c=='q':
			break
		if c=='' and len(qds)>0:
			qds.pop( -1)
		else:
			qds.append( c)
