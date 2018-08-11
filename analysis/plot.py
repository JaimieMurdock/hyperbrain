from argparse import ArgumentParser
from collections import defaultdict
from csv import DictReader

from matplotlib.pyplot import *

def plot_KL(graph):
    """
    graph: {author: {year: KL}}
    """

    for author, year_KL in graph.items():
        years = sorted(year_KL.keys())
        plot(np.array(year_KL[year] for year in years))
    
    show()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('graphfile')
    args = parser.parse_args()

    # build graph
    graph = defaultdict(dict)
    with open(args.graphfile) as graphfile:
        reader = DictReader(infile, fieldnames=[
                'author', 'year', 'read_to_write', 'write_to_read',
                '# readings', '# writings'], delimiter='\t')

        for row in reader:
            graph[row['author']][row['year']] = row['read_to_write']
            if len(graph) > 10:
                break
    
    plot_KL(graph)