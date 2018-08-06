from argparse import ArgumentParser
from collections import defaultdict
from csv import DictReader

def build_graph(graphfile):
    author_readings = defaultdict(lambda: defaultdict(set))
    with open(graphfile) as infile:
        reader = DictReader(infile, fieldnames=[
            'author', 'seq', 
            'date', 'article', 'year', 
            'cited', 'cited_year'], delimiter='\t')
        
        for row in reader:
            author_readings[row['author']][int(row['year'])].add(row['cited'])

    return author_readings

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('graphfile')
    args = parser.parse_args()

    graph = build_graph(args.graphfile)
    for author, year_readings in graph.items():
        years = sorted(year_readings.keys())
<<<<<<< Updated upstream
        if len(years) > 3:
            print(author)
            encountered = set()
            for year in years:
                print(year, len(year_readings[year]),
                len(year_readings[year].difference(encountered)),
                len(encountered))
=======
        if len(years) > 1:
            print(author)
            encountered = set()
            for year in years:
                print(
                    year, 
                    len(year_readings[year]),
                    len(encountered.difference(year_readings[year])),
                    len(encountered), sep='\t')
>>>>>>> Stashed changes
                encountered.update(year_readings[year])
