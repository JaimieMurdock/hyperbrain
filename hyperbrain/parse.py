import json
import os.path
this_place = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(this_place, '../human-brain-atlas.json')) as jsonfile:
    atlas = json.load(jsonfile)['msg']

name_id = dict()
name_abbr = dict()
abbr_id = dict()
abbr_name = dict()
def add_ids(atlas):
    global name_id
    for item in atlas:
        if ',' not in item['name']:
            name_id[item['name']] = item['id']
            name_abbr[item['name']] = item['acronym']
            abbr_id[item['acronym']] = item['id']
            abbr_name[item['acronym']] = item['name']
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

    while rest:
        if u' ' not in rest:
            yield rest
            return

        first, rest = rest.split(u' ', 1)
        rest = rest.strip()

        # always yield the raw string
        yield first

        # search the database for keywords
        if name_id.get(first):
            patterns.append(first)

        patterns = [name for name in name_id.keys() 
                        if name.startswith(first + u' ')]

        for p in patterns:
            # check if multi-phrase starts match in the rest of the phrase.
            if u' ' in p:
                first_pattern_word, longpattern = p.split(u' ',  1)
                if first == first_pattern_word and (rest == longpattern 
			or rest.startswith(longpattern + u' ')):
                    yield u"abi:{}".format(name_id[p])
            elif first == p:
                yield u"abi:{}".format(name_id[p])


def brain_tokenizer(document):
    return list(_inpho_token_generator(document))
