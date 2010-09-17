class songdb:
    fieldnames=[ 'sno', 'gender', 'name', 'singer', 'lang', 'nwords', 'stype']
    numfields=['sno', 'lang', 'nwords', 'stype']
    def __init__(self, fn='songu.csv'):
        self.load( fn)

    def load(self, fn):
        records = []
        fh = open( fn, 'rt')
        fh.seek(3)
        #import locale
        #locale.getdefaultlocale()[1]
        for line in fh:
            d = line.split('\t')
            try:
                field_data = [ int(d[0]), d[1], d[2], d[3], int(d[4]), int(d[5]), int(d[6])]
            except ValueError:
                print 'error is ', d
                continue
            rec = dict( zip( self.fieldnames, field_data))
            #rec = field_data
            records.append(rec)
        records.sort()
        self.records = records
        fh.close()

    def dump(self):
        for rec in self.records:
            print ('{sno}\t{gender}\t{name}\t{singer}\t{lang}\t{nwords}\t{stype}'.format( sno=rec['sno'], gender=rec['gender'], name=rec['name'], singer=rec['singer'], lang=rec['lang'], nwords=rec['nwords'], stype=rec['stype']))

    def query( self, data, field='sno'):
        if field not in self.fieldnames:
            raise ValueError, 'no such field {0}'.format(field)
        if field in self.numfields:
            data=int(data)
        recs=[]
        for rec in self.records:
            if rec[field]==data:
                recs.append(rec)
        return recs

    def querybyname( self, name):
        self.query( name, 'name')

    def querybysinger( self, singer):
        self.query( singer, 'singer')

    def grep( self, data, field='name'):
        if field not in [ 'name', 'singer']:
            raise ValueError, 'Can not grep on field {0}'.format(field)
        recs=[]
        for rec in self.records:
            if data in rec[field]:
                recs.append(rec)
        return recs

    def fielddata( self, field):
        return [rec[field] for rec in self.records]
        
    def descstr( self, se):
        return '{0}: {1}, {2}'.format( se['sno'], se['name'], se['singer'])

    def dumpjson( self):
        import json
        return json.dumps( self.records, True, False, indent=4)
        
    def charset( self, field='name'):
        if field not in [ 'name', 'singer']:
            raise ValueError, 'Can not collect char set on field {0}'.format(field)
        bigstr=''
        for rec in self.records:
            bigstr+=rec[field]
        return list(set(bigstr))
        
if __name__ == '__main__':
    import sys,random
    db = songdb(sys.argv[1])
    print 'qsong by sno'
    snos = db.fielddata('sno')
    random.shuffle(snos)
    for si in xrange(10):
        ses = db.query( snos[si] )
        for se in ses:
            print( db.descstr(se))
    
    try:
        print db.dumpjson()
    except UnicodeDecodeError:
        pass

    """
    print 'qsong by name'
    names = db.fielddata('name')
    random.shuffle(names)
    for si in xrange(10):
        print 'try to query ', names[si]
        ses = db.querybyname( names[si] )
        for se in ses:
            print( db.descstr(se))
    
    print 'qsong by singer'
    singers = db.fielddata('singer')
    random.shuffle( singers)
    for si in xrange(10):
        ses = db.querybysinger( singers[si] )
        for se in ses:
            print( db.descstr(se))

    print 'grep name'
    chs = db.charset('name')
    random.shuffle(chs)
    for si in xrange(10):
        print 'try to grep: ', chs[si]
        ses = db.grep( chs[si], 'name')
        for se in ses:
            print( db.descstr(se))
    """
