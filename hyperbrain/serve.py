import json
from operator import itemgetter
import os, os.path

from vsm.corpus import Corpus
from vsm import LDA, LdaCgsViewer
from hyperbrain.parse import parent, children
# import topicexplorer.extensions.bibtex as bibtex

from bottle import abort, request, response, route, run, static_file, Bottle

from proxy import create_proxy

# Global variables
IMAGE_DIR = '../images/'
IMAGE_DIR = os.path.join(os.path.dirname(__file__), IMAGE_DIR)

WWW_DIR = '../www/'
WWW_DIR = os.path.join(os.path.dirname(__file__), WWW_DIR)

root = Bottle()

proxy_app = create_proxy("http://localhost:8010/")
root.mount('/topics', proxy_app)

@root.route('/papers/<structure_id:int>.json')
def get_papers(structure_id, ctx_type='article', full_cite=False):
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
        md = corpus.view_metadata(ctx_type)
        label_data = [
            (label[ctx_type + '_label'], 
                {'count' : np.in1d(doc, words).sum(),
                 'doi' : label['doi'],
                 'title' : label['title']}) 
                for label, doc in zip(md, corpus.view_contexts(ctx_type)) 
                    if np.in1d(doc, words).any()]
        label_data = dict(label_data)

        labels = sorted(label_data.keys(), 
                        key=lambda x: label_data[x]['count'],
                        reverse=True)

        label_objs = []
        for label in labels:
            obj = {'id' : label, 'name' : label_data[label]['title'],
                   #'url' : '/fulltext/'+label.replace('.txt','.pdf'),
                   'url' : 'http://dx.doi.org/' + label_data[label]['doi'],
                   'doi' : label_data[label]['doi'],
                   'count' : label_data[label]['count']}
            if full_cite:
                obj['name'] = bibtex.label(label.replace('.txt','.pdf'))
            label_objs.append(obj)
    
        return json.dumps(label_objs)
    else:
        return json.dumps(None)
        
@root.route('/fulltext/<doc_id>')
def get_doc(doc_id):
    import re
    corpus_path = '/home/jammurdo/hyperbrain/test/VOF_VPF/'
    pdf_path = os.path.join(corpus_path, re.sub('txt$','pdf', doc_id))
    if os.path.exists(pdf_path):
        doc_id = re.sub('txt$','pdf', doc_id)
    
    return static_file(doc_id, root=corpus_path)


@root.route('/img/<id:int>.svg')
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


@root.route('/<filename:path>')
def www_file(filename):
    """ Serves a static file, given a path. """
    if filename.endswith('isomap'):
        filename += '/'
    if filename.endswith('/'):
        filename += 'index.html'

    path = os.path.join(WWW_DIR, filename)
    if os.path.exists(path):
        return static_file(filename, root=WWW_DIR)
    elif os.path.exists(os.path.join('/home/jammurdo/Neuro/', filename)):
        return static_file(filename,
            root='/home/jammurdo/Neuro')
    else:
        return static_file(filename,
            root='/home/jammurdo/workspace/topics-1.0/www/')

@root.route('/')
def index():
    return static_file('index.html', root=WWW_DIR)

def main():
    from argparse import ArgumentParser
    from topicexplorer.lib.util import is_valid_configfile

    # Construct argument parser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=8000)
    # parser.add_argument('config', help="Configuration File", 
    #     type=is_valid_configfile)
    parser.add_argument('corpus')
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
    corpus = Corpus.load(args.corpus)
    from argparse import Namespace

    # bibtex.init(None, None, Namespace(bibtex='library.bib'))

    # Launch server
    port = args.port
    host = '0.0.0.0'
    root.run(server='paste', host=host, port=port)

if __name__ == '__main__':
    main()
