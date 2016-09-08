from collections import defaultdict
import numpy as np

from hyperbrain.parse import *
from vsm.corpus import Corpus

import sys
c = Corpus.load(sys.argv[-1])

# get all terms in corpus
abi_vocab = [word for word in c.words if word.startswith('abi:')]

# get all counts
abi_counts = defaultdict(int)
for word in abi_vocab:
    id = int(word.replace('abi:',''))
    count = (c.corpus==c.words_int[word]).sum()
    abi_counts[id] = count

# calculate how many children there are of each node
def get_child_counts(key):
    if children[key]:
        return abi_counts[key] + sum([get_child_counts(child_key) 
                                          for child_key in children[key] 
                                              if child_key != key])
    else:
        return abi_counts[key]

child_counts = defaultdict(int)
for key, childs in children.iteritems():
    child_counts[key] = get_child_counts(key)

parent_counts = defaultdict(int)
for key, pkey in parent.iteritems():
    while parent.get(pkey):
        parent_counts[key] += abi_counts[pkey]
        pkey = parent.get(pkey)

abi_counts2 = defaultdict(int)
# trickle down the child counts to all child nodes
def add_to_children_of(key, value):
    for child in children[key]:
        if child != key:
            abi_counts[child] += value
            add_to_children_of(child, value)

for key, child in children.iteritems():
    if child_counts[key]:
        add_to_children_of(key, np.log2(child_counts[key]))

print ",".join(['id','name','count','child_count','children'])
for id, child_count in child_counts.iteritems():
    print ",".join(map(str, [id, '"'+id_name.get(id,'')+'"', abi_counts[id], child_count,
                             len(children.get(id, list()))]))
