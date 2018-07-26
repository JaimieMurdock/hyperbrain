from argparse import ArgumentParser
from collections import defaultdict
from csv import DictReader

def build_graph(graphfile):
    author_readings = defaultdict(lambda: defaultdict(list))
    with open(graphfile) as infile:
        reader = DictReader(infile, fieldnames=[
            'author', 'seq', 
            'date', 'article', 'year', 
            'cited', 'cited_year'], delimiter='\t')
        
        for row in reader:
            author_readings[row['author']][row['year']].append(row['cited'])

    return author_readings

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('graphfile')
    args = parser.parse_args()

    graph = build_graph(args.graphfile)
    for author, year_readings in graph.items():
        print(author)
        for year, readings in year_readings.items():
            try:
                print(year, len(readings))
            except TypeError:
                pass
