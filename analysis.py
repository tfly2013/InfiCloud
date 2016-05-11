"""
Team: Cluster and Cloud Computing Team 3
Contents: Assigment 2
Authors: Kimple Ke, Roger Li, Fei Tang, Bofan Jin, David Ye
"""

import couchdb, csv, string, operator
from collections import Counter
from argparse import ArgumentParser
from location import *

def parse_args():
    """ Read arguments from command line."""

    parser = ArgumentParser(
        description="Analysing Application based on keywords search, SLA and AURIN data."
    )
    parser.add_argument(
        '--topic',
        type=int,
        default=1,
        help='Topic that this search is about.'        
    )
    parser.add_argument(
        '--db',
        type=str,
        help='Database name for this search.' 
    )
    parser.add_argument(
        '--keywords',
        type=str,
        nargs='+',
        help='Keywords for this search.'        
    )
    parser.add_argument(
        '--aurin',
        type=str,
        help='Aurin data.'        
    )
    return parser.parse_args()

def analysis(args):
    """ Analysis couchDB data using MapReduce and correlate result to AURIN data."""
    keywords = args.keywords
    topic = "topic" + str(args.topic)

    # connect to couchDB
    couch = couchdb.Server("http://115.146.94.116:5984/")
    db = couch[args.db]

    # create regular expression based on keywords from args
    re = ""
    for word in keywords:
        re += word + '|'
    re = re[:-1]

    # map function, which is based on RE search
    mapfun = '''function(doc) {
    var re = /\\b'''+ re +'''\\b/i;
    if (doc.text.search(re) != -1)
        emit(doc.sla, 1);
    }'''

    # built-in reduce function _count
    reducefun = "_count"
    mapreduce = {'map': mapfun,'reduce': reducefun}    

    # create or update the design document
    ddoc = db.get("_design/sla")
    if ddoc:
        ddoc["views"][topic] = mapreduce
        db.save(ddoc)
    else:
        design = {'views': {topic: mapreduce}}
        db["_design/sla"] = design

    # retrive result from view
    result = db.view('sla/'+ topic, group=True)

    # build a correlation map between view result and AURIN data
    correlation_map = {}
    # read in AURIN data in csv format
    with open(args.aurin) as csvfile:
        reader = csv.reader(csvfile)
        # put data that has same SLA together
        for row in reader:
            for line in result:
                if row[0] == line.key:
                    correlation_map[line.key] = (line.value, row[1])
    
    # sort correlation map by number of tweeets in this SLA                
    correlation_map = sorted(correlation_map.items(), \
    key=(operator.itemgetter(1)), reverse=True)     
    
    # read in population data in each SLA
    populations = list(csv.reader(open("./data/sla_population.csv")))
    populations_dict = {}
    for p in populations:
        populations_dict[p[0]] = p[2]
    
    # divide number of tweets by the popluation in SLA, and output as csv file
    with open('correlation.csv', 'w') as csvfile:   
        csvfile.write('SLA,Tweet Count,Tweets per 1000 Population,Aurin Data,Aurin Data per 100 population\n')    
        for data in correlation_map:
            if data[1][1] != 'null':    
                csvfile.write('{0},{1},{2},{3},{4}\n'.format(data[0], data[1][0], \
                data[1][0] * 1000 / float(populations_dict.get(data[0], 100000000)), \
                data[1][1], float(data[1][1]) * 100 / float(populations_dict.get(data[0], 100000000))))
    
def main():
    args = parse_args()
    analysis(args)
    
if __name__ == '__main__':
    main()
