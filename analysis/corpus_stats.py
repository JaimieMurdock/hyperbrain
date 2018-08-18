from vsm import Corpus

def print_corpus_stats(corpus_file):
    c = Corpus.load(corpus_file)
    print('Corpus length:', len(c))
    
    abi_words = [w for w in c.words if w.startswith('abi:')]
    print('Anatomical regions:', len(abi_words))

    total_tags = sum([len(c.corpus[c.corpus==c.words_int[w]]) for w in abi_words])
    print('Number of anatomical tokens:', total_tags)

if __name__=='__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('corpus_file')
    args = parser.parse_args()

    print_corpus_stats(args.corpus_file)