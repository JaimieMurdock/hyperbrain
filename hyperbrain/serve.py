import os, os.path

from bottle import abort, request, response, route, run, static_file

# Global variables
IMAGE_DIR = '../images/'
IMAGE_DIR = os.path.join(os.path.dirname(__file__), IMAGE_DIR)

WWW_DIR = '../www/'
WWW_DIR = os.path.join(os.path.dirname(__file__), WWW_DIR)

@route('/papers/<structure:int>')
def get_papers(structure_id):
    """ Returns a list of papers which reference the given brain structure. """
    pass

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
    #parser.add_argument('config', help="Configuration File", 
    #    type=is_valid_configfile)
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
    # Launch server
    port = args.port
    host = '0.0.0.0'
    run(host=host, port=port)
