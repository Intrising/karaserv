class songdb:
    fieldnames=[ 'sno', 'gender', 'name', 'singer', 'lang', 'nwords', 'stype', 'photourl', 'songfn']
    numfields=['sno', 'lang', 'nwords']
    def __init__(self, fn='songu.csv'):
        self.load( fn)

    def load(self, fn):
        songs = []
        singers = []
        fh = open( fn, 'rt')
        for line in fh:
            line = line.strip('\r\n')
            d = line.split('\t')
            for i in range(len(d), 9):
                d.append('')
            try:
                field_data = [ int(d[0]), d[1], d[2], d[3], int(d[4]), int(d[5]), d[6], d[7], d[8]]
            except ValueError:
                print 'error is ', d
                continue
            song = dict( zip( self.fieldnames, field_data))
            song['singer'] = song['singer'].split('&')
            #song = field_data
            songs.append(song)
            for singer in song['singer']:
                self.add_singer( singers, singer, song['gender'], song['lang'])
        songs.sort()
        self.songs = songs
        self.singers = singers
        fh.close()
    def calc_nsongs( self):
        nmvs=0
        for song in self.songs:
            if len(song['songfn'])>0:
                print song['songfn']
                nmvs+=1
        print '{0} mvs of {0} songs'.format( nmvs, len(self.songs))

    def del_songs( self, snolist):
        idxlst=[]
        for i, song in enumerate(self.songs):
            if song['sno'] in snolist:
                idxlst.append(i)
        idxlst.sort(reverse=True)
        for i in idxlst:
            self.songs.pop(i)

    def add_singer( self, allsingers, singername, gender, lang):
        for singer in allsingers:
            if singername == singer['name']:
                if lang not in singer['langs']:
                    singer['langs'].append(lang)
                if gender in ['F', 'M']:
                    singer['gender']=gender
                return
        allsingers.append( dict(name=singername, langs=[lang], gender='X'))

    def dump(self):
        for song in self.songs:
            print ('{sno}\t{gender}\t{name}\t{singer}\t{lang}\t{nwords}\t{stype}\t{photourl}\t{songfn}'.format( sno=song['sno'], gender=song['gender'], name=song['name'], singer='&'.join(song['singer']), lang=song['lang'], nwords=song['nwords'], stype=song['stype'], photourl=song['photourl'], songfn=song['songfn']))

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

    def ismatch( self, song, qexprs):
        for field,val in qexprs.items():
            if field=='singer':
                if val not in song[field]:
                    return False
            elif song[field]<>val:
                return False
        return True

    def mquery( self, qexprs):
        recs=[]
        for song in self.songs:
            if self.ismatch( song, qexprs):
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

    def search( self, data, field='any'):
        if field not in [ 'name', 'singer', 'any']:
            raise ValueError, 'Can not grep on field {0}'.format(field)
        recs=[]
        if field=='any':
            for song in self.songs:
                if data in song['name']:
                    recs.append(song)
                else:
                    singerlstr = ''.join(song['singer'])
                    if data in singerlstr:
                        recs.append( song)
        elif field=='singer':
            for song in self.songs:
                singerlstr = ''.join(song['singer'])
                if data in singerlstr:
                    recs.append( song)
        else:
            for song in self.songs:
                if data in song[field]:
                    recs.append(song)
        return recs

    def fielddata( self, field):
        return [song[field] for song in self.songs]

    def descstr( self, se):
        singerlstr = ''.join(se['singer'])
        return '{0}: {1} by {2}'.format( se['sno'], se['name'], singerlstr)

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

systemdb = songdb( 'mdssong.csv')

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

    def searchtest(db):
        qstr = raw_input('please input any string for search:')
        ses = db.search( qstr)
        for se in ses:
            print( '\t'+db.descstr(se))

    def searchtest2(db):
        qstr = raw_input('please input song name for search:')
        ses = db.search( qstr, 'name')
        for se in ses:
            print( '\t'+db.descstr(se))
        qstr = raw_input('please input singer name for search:')
        ses = db.search( qstr, 'singer')
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

    def list_midi_songs( db):
        ses = db.query( data='midi', field='stype')
        for se in ses:
            print( '\t'+db.descstr(se))
    def testdump(db):
        db.dump()

    def test_del_songs(db):
        snos=[81405,330252]
        db.del_songs( snos)
        db.dump()

    def test_chinese_nwords( db):
        songs = db.mquery( { 'lang':1, 'nwords':10})
        for song in songs:
            print song['name']

    """
    def change_stype( db):
        stype=''
        for song in db.songs:
            if len(song['mvfn'])>0:
                if song['sno']>=14000 and song['sno']<15000:
                    stype='au'
                else:
                    stype='mv'
            else:
                stype='midi'
            song['stype']=stype
    """
    db= systemdb
    #testdump(db)
    test_del_songs(db)
    #list_midi_songs( db)
    #test_chinese_nwords( db)
    #change_stype(db)
    #db.dump()
    #db.calc_nsongs()
    #list_singers_by_lang( db)
    #list_singers_by_gender(db)
    #list_all_singers(db)
