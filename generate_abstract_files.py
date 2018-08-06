from argparse import ArgumentParser
from collections import defaultdict
import os, os.path
import sys

from progressbar import ProgressBar, Bar

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('abstract')
    parser.add_argument('-o', '--output', default='data-08-2018')
    args = parser.parse_args()

    abstracts = defaultdict(str)
    titles = defaultdict(str)

    with open(args.abstract) as absfile:
        for line in absfile:
            id, doi, title, abstract = line.split('\t', 3)
            titles[id] = title
            abstracts[id] = title
    
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    pbar = ProgressBar(widgets=[Bar()])
    for key in pbar(abstracts.keys()):
        filename = os.path.join(args.ouptut, key)
        with open(filename, 'w') as outfile:
            outfile.write(titles[key] + '\n')
            outfile.write(abstracts[key] + '\n')
            outfile.write(' \n')

