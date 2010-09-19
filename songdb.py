class songdb:
    fieldnames=[ 'sno', 'gender', 'name', 'singer', 'lang', 'nwords', 'stype']
    numfields=['sno', 'lang', 'nwords', 'stype']
    def __init__(self, fn='songu.csv'):
        self.load( fn)

    def load(self, fn):
        songs = []
        singers = []
        fh = open( fn, 'rt')
        fh.seek(3)
        #import locale
        #locale.getdefaultlocale()[1]
        for line in fh:
            d = line.split('\t')
            try:
                field_data = [ int(d[0]), d[1], d[2], d[3].strip(' '), int(d[4]), int(d[5]), int(d[6])]
            except ValueError:
                print 'error is ', d
                continue
            song = dict( zip( self.fieldnames, field_data))
            song['singer'] = song['singer'].split('\xe3\x80\x81')
            #song = field_data
            songs.append(song)
            for singer in song['singer']:
                self.add_singer( singers, singer, song['gender'], song['lang'])
        songs.sort()
        self.songs = songs
        self.singers = singers
        fh.close()
    
    def add_singer( self, allsingers, singername, gender, lang):
        for singer in allsingers:
            if singername == singer['name']:
                #todo: abondon set operation
                singer['langs'].add(lang)
                if gender in ['F', 'M']:
                    singer['gender']=gender
                return
        allsingers.append( dict(name=singername, langs=[lang], gender='X'))

    def dump(self):
        for song in self.songs:
            print ('{sno}\t{gender}\t{name}\t{singer}\t{lang}\t{nwords}\t{stype}'.format( sno=song['sno'], gender=song['gender'], name=song['name'], singer=song['singer'], lang=song['lang'], nwords=song['nwords'], stype=song['stype']))

    def dump_singers( self):
        for singer in self.singers:
            print ('{0}, {1}, lang={2}'.format(singer['name'], singer['gender'], singer['langs']))

    def query( self, data, field='sno'):
        if field not in self.fieldnames:
            raise ValueError, 'no such field {0}'.format(field)
        if field in self.numfields:
            data=int(data)
        recs=[]
        if field=='singer':
            for song in self.songs:
                if data in song['singer']:
                    recs.append( song)
        else:
            for song in self.songs:
                if song[field]==data:
                    recs.append(song)
        return recs

    def qsingers( self, field=None, data=None):
        if field==None:
            return self.singers
        if field=='lang':
            field='langs'
        if field=='langs' and type(data)==str:
            data=int(data)
        return [singer for singer in self.singers if data in singer[field]]
        
    def querybyname( self, name):
        self.query( name, 'name')

    def querybysinger( self, singer):
        self.query( singer, 'singer')
        
    def grep( self, data, field='name'):
        if field not in [ 'name', 'singer']:
            raise ValueError, 'Can not grep on field {0}'.format(field)
        recs=[]
        if field=='singer':
            for song in self.songs:
                if data in song['singer']:
                    recs.append( song)
        else:
            for song in self.songs:
                if data in song[field]:
                    recs.append(song)
        return recs

    def fielddata( self, field):
        return [song[field] for song in self.songs]
        
    def descstr( self, se):
        return '{0}: {1}, {2}'.format( se['sno'], se['name'], se['singer'])

    def dumpjson( self):
        import json
        return json.dumps( self.songs, True, False, indent=4)
        
    def charset( self, field='name'):
        if field not in [ 'name', 'singer']:
            raise ValueError, 'Can not collect char set on field {0}'.format(field)
        bigstr=''
        for song in self.songs:
            bigstr+=song[field]
        return list(set(bigstr))
        
if __name__ == '__main__':
    import sys,random

    def qsongbyno(db):
        print 'qsong by sno'
        snos  = db.fielddata('sno')
        random.shuffle(snos)
        for si in xrange(10):
            ses = db.query( snos[si] )
            for se in ses:
                print( db.descstr(se))

    def dumpjson(db):
        try:
            print db.dumpjson()
        except UnicodeDecodeError:
            pass

    def qsongbyname(db):
        print 'qsong by name'
        names = db.fielddata('name')
        random.shuffle(names)
        for si in xrange(10):
            print 'try to query ', names[si]
            ses = db.querybyname( names[si] )
            for se in ses:
                print( db.descstr(se))
   
    def qsongbysinger(db):
        print 'qsong by singer'
        singers = db.fielddata('singer')
        random.shuffle( singers)
        for si in xrange(10):
            ses = db.querybysinger( singers[si] )
            for se in ses:
                print( db.descstr(se))

    def grepname(db):
        print 'grep name'
        chs = db.charset('name')
        random.shuffle(chs)
        for si in xrange(10):
            print 'try to grep: ', chs[si]
            ses = db.grep( chs[si], 'name')
            for se in ses:
                print( '\t'+db.descstr(se))

    def greptest(db):
        qstr = raw_input('please input song name for search:')
        ses = db.grep( qstr, 'name')
        for se in ses:
            print( '\t'+db.descstr(se))
        qstr = raw_input('please input singer name for search:')
        ses = db.grep( qstr, 'singer')
        for se in ses:
            print( '\t'+db.descstr(se))
      
        
    def list_singers_by_lang( db):
        for lang in ['1', '2']:
            print 'lang ', lang
            singers = db.qsingers( 'lang', lang)
            for singer in singers:
                print singer['name']
        
    def list_singers_by_gender( db):
        for gender in ['M', 'F']:
            print 'gender ', gender
            singers = db.qsingers( 'gender', gender)
            for singer in singers:
                print singer['name']

    def list_all_singers( db):
        singers = db.qsingers()
        for singer in singers:
            print singer['name']

    db = songdb(sys.argv[1])
    #greptest(db)
    list_singers_by_gender(db)
    #list_all_singers(db)

