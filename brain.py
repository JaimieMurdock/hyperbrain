import json
with open('human-brain-atlas.json') as jsonfile:
    atlas = json.load(jsonfile)['msg']

name_id = dict()
def add_ids(atlas):
    global name_id
    for item in atlas:
        if ',' not in item['name']:
            name_id[item['name']] = item['id']
        if item.get('children'):
            add_ids(item['children'])

add_ids(atlas)
for name, id in name_id.iteritems():
    print id, name

print len(name_id)

def _brain_token_generator(document):
    if PUNC_TABLE.get(ord('-')):
        del PUNC_TABLE[ord('-')]
    PUNC_TABLE[ord('\n')] = ord(' ')
    
    rest = document.lower()
    rest = rehyph(rest)
    rest = strip_punc_word(rest)
    query = Session.query(Searchpattern)

    MIN_LEN = 6 

    while rest:
        if u' ' not in rest:
            yield rest
            return

        first, rest = rest.split(u' ', 1)
        rest = rest.strip()

        # always yield the raw string
        yield first

        # check if we can simply skip the short patterns
        if len(first) < MIN_LEN and first not in short_patterns:
            continue


       
        # search the database for keywords
        patterns = query.filter(Searchpattern.searchpattern.like(first + u' %')).all()
        
        exact_match = query.filter(Searchpattern.searchpattern==first).first()
        if exact_match is not None:
            patterns.append(exact_match)

        for p in patterns:
            # check if multi-phrase starts match in the rest of the phrase.
            if u' ' in p.searchpattern:
                first_pattern_word, longpattern = p.searchpattern.split(u' ',  1)
                if first == first_pattern_word and (rest == longpattern 
			or rest.startswith(longpattern + u' ')):
                    yield u"inpho:{}".format(p.entity.ID)
            elif first == p.searchpattern:
                yield u"inpho:{}".format(p.entity.ID)


def inpho_tokenizer(document):
    return list(_inpho_token_generator(document))
