import json
from operator import itemgetter
import os, os.path

from vsm.corpus import Corpus
from vsm import LDA, LdaCgsViewer
from hyperbrain.parse import parent, children
import topicexplorer.extensions.bibtex as bibtex

from bottle import abort, request, response, route, run, static_file

# Global variables
IMAGE_DIR = '../images/'
IMAGE_DIR = os.path.join(os.path.dirname(__file__), IMAGE_DIR)

WWW_DIR = '../www/'
WWW_DIR = os.path.join(os.path.dirname(__file__), WWW_DIR)

@route('/papers/<structure_id:int>.json')
def get_papers(structure_id, full_cite=True):
    """ Returns a list of papers which reference the given brain structure. """
    global corpus
    import numpy as np
    response.context_type = 'application/json'

    struct_heirarchy = set(children[structure_id])
    id = structure_id
    while parent.get(id):
        struct_heirarchy.add(parent[id])
        id = parent[id]
    struct_heirarchy.remove(structure_id)
    struct_heirarchy = [str(w) for w in struct_heirarchy]

    #words = [corpus.words_int[w] for w in corpus.words if w.startswith('abi:')]
    #words = [corpus.words_int.get('abi:{}'.format(structure_id))]
    words = [corpus.words_int[w] for w in corpus.words 
                 if w.startswith('abi:') and w[4:] in struct_heirarchy]
    if words:
        md = corpus.view_metadata('document')['document_label']
        label_count = [
            (label, np.in1d(doc, words).sum()) 
                for label, doc in zip(md, corpus.view_contexts('document')) 
                    if np.in1d(doc, words).any()]
        label_count = dict(label_count)

        labels = sorted(label_count.keys(), 
                        key=label_count.get,
                        reverse=True)

        label_objs = []
        for label in labels:
            obj = {'id' : label, 'name' : label, 
                   'url' : '/fulltext/'+label.replace('.txt','.pdf'),
                   'count' : label_count[label]}
            if full_cite:
                obj['name'] = bibtex.label(label.replace('.txt','.pdf'))
            label_objs.append(obj)
    
        return json.dumps(label_objs)
    else:
        return json.dumps(None)
        
@route('/fulltext/<doc_id>')
def get_doc(doc_id):
    import re
    corpus_path = '/home/jaimie/workspace/hyperbrain/test/VOF_VPF/'
    pdf_path = os.path.join(corpus_path, re.sub('txt$','pdf', doc_id))
    if os.path.exists(pdf_path):
        doc_id = re.sub('txt$','pdf', doc_id)
    
    return static_file(doc_id, root=corpus_path)

@route('/img/<id:int>.svg')
def get_image(id):
    """ Find an image with the given id.

    Returns either an svg file or a 404 error. """
    path = None
    for root, dirs, files in os.walk(IMAGE_DIR):
        results = [file for file in files if file.startswith('{0:04d}'.format(id))]
        if results:
            path = results[0]
            break

    if path:
        return static_file(path, root=IMAGE_DIR)
    else:
        abort(404, "Image not found.")

@route('/<filename:path>')
def www_file(filename):
    """ Serves a static file, given a path. """
    return static_file(filename, root=WWW_DIR)

@route('/')
def index():
    return static_file('index.html', root=WWW_DIR)

if __name__ == '__main__':
    from argparse import ArgumentParser
    from topicexplorer.lib.util import is_valid_configfile

    # Construct argument parser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=8000)
    # parser.add_argument('config', help="Configuration File", 
    #     type=is_valid_configfile)
    args = parser.parse_args()

    """
    # load in the configuration file
    config = ConfigParser({
        'raw_corpus' : None,
        'fulltext' : 'false'})
    config.read(args.config)
    
    # path variables
    corpus_file = config.get('main', 'corpus_file')
    
    # Load text model objects
    corpus = Corpus.load(corpus_file)
    """
    global corpus 
    corpus = Corpus.load('/home/jaimie/workspace/hyperbrain/test/models/VOF_VPF-txt-freq5-nltk-en-freq10-N1095.npz')
    from argparse import Namespace

    bibtex.init(None, None, Namespace(bibtex='library.bib'))

    # Launch server
    port = args.port
    host = '0.0.0.0'
    run(host=host, port=port)
