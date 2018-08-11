from argparse import ArgumentParser
from collections import defaultdict
from csv import DictReader
import logging

import topicexplorer
from vsm.spatial import KL_div

def build_reading_graph(graphfile):
    author_readings = defaultdict(lambda: defaultdict(set))
    with open(graphfile) as infile:
        reader = DictReader(infile, fieldnames=[
            'author', 'seq', 
            'date', 'article', 'year', 
            'cited', 'cited_year'], delimiter='\t')
        
        for row in reader:
            author_readings[row['author']][int(row['year'])].add(row['cited'])

    return author_readings

def build_writing_graph(graphfile):
    author_writings = defaultdict(lambda: defaultdict(set))
    with open(graphfile) as infile:
        reader = DictReader(infile, fieldnames=[
            'author', 'seq', 
            'date', 'article', 'year', 
            'cited', 'cited_year'], delimiter='\t')
        
        for row in reader:
            author_writings[row['author']][int(row['year'])].add(row['article'])

    return author_writings


def build_encounters(year_readings):
    """
    Converts a dictionary of years and readings to a first-encountered graph
    """
    years = sorted(year_readings.keys())

    encountered = set()
    for year in years:
        logging.debug(
            year, 
            len(year_readings[year]),
            len(encountered.difference(year_readings[year])),
            len(encountered))
        encountered.update(year_readings[year])
    
    return encountered

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('graphfile')
    parser.add_argument('conifg')
    args = parser.parse_args()

    te = topicexplorer.from_config(args.config)

    readings = build_reading_graph(args.graphfile)
    writings = build_writing_graph(args.graphfile)

    authors = readings.keys()

    for author in authors:
        logging.debug(f"PROCESSING {author}")
        assert readings[author].keys() == writings[author].keys()

        for year in sorted(readings[author].keys()):
            reading_topics = te[20].doc_topic_matrix(readings[author][year]).mean(axis=0)
            writing_topics = te[20].doc_topic_matrix(writings[author][year]).mean(axis=0)
            
            write_from_read = KL_div(reading_topics, writing_topics)
            read_from_write = KL_div(writing_topics, reading_topics)

            print(author, year, write_from_read, read_from_write, sep='\t')

"""
for each author
    group of articles written in a year
    group of articles read in a year
    KL_div(read, written)
"""