import os


booknames = [
    ('Gen', 'gen'),
    ('Exod', 'exo'),
    ('Lev', 'lev'),
    ('Num', 'num'),
    ('Deut', 'deu'),
    ('Josh', 'jos'),
    ('Judg', 'jdg'),
    ('Ruth', 'rut'),
    ('1Sam', 'sa1'),
    ('2Sam', 'sa2'),
    ('1Kgs', 'kg1'),
    ('2Kgs', 'kg2'),
    ('1Chr', 'ch1'),
    ('2Chr', 'ch2'),
    ('Ezra', 'ezr'),
    ('Neh', 'neh'),
    ('Esth', 'est'),
    ('Job', 'job'),
    ('Ps', 'psa'),
    ('Prov', 'pro'),
    ('Eccl', 'ecc'),
    ('Song', 'sol'),
    ('Isa', 'isa'),
    ('Jer', 'jer'),
    ('Lam', 'lam'),
    ('Ezek', 'eze'),
    ('Dan', 'dan'),
    ('Hos', 'hos'),
    ('Joel', 'joe'),
    ('Amos', 'amo'),
    ('Obad', 'oba'),
    ('Jonah', 'jon'),
    ('Mic', 'mic'),
    ('Nah', 'nah'),
    ('Hab', 'hab'),
    ('Zeph', 'zep'),
    ('Hag', 'hag'),
    ('Zech', 'zac'),
    ('Mal', 'mal')
]


books = sorted(os.listdir('./usfm/'))

for book in books:
    booknum = book[:2]
    if booknum == '85':
        osis_name = 'AddPs'
    else:
        osis_name = booknames[int(booknum) - 1][0]
    print(osis_name)
    os.system('usfm2osis Bible.Thomson -o ./osis/{0}-{1}.xml ./usfm/{2}'.format(booknum, osis_name, book))
