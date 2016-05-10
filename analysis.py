import couchdb, csv, string, operator
from collections import Counter
from argparse import ArgumentParser
from location import *

def parse_args():
    """ Read arguments from command line."""

    parser = ArgumentParser(
        description="Keywords searching and counting in couchDB."
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
        help='Database name for search.' 
    )
    parser.add_argument(
        '--keywords',
        type=str,
        nargs='+',
        help='Keywords for search.'        
    )
    parser.add_argument(
        '--aurin',
        type=str,
        help='Aurin data.'        
    )
    return parser.parse_args()

def analysis(args):
    keywords = args.keywords
    topic = "topic" + str(args.topic)

    couch = couchdb.Server("http://115.146.94.116:5984/")
    db = couch[args.db]

    re = ""
    for word in keywords:
        re += word + '|'
    re = re[:-1]

    mapfun = '''function(doc) {
    var re = /\\b'''+ re +'''\\b/i;
    if (doc.text.search(re) != -1)
        emit(doc.sla, 1);
    }'''

    reducefun = "_count"
    
    mapreduce = {'map': mapfun,'reduce': reducefun}
    
    ddoc = db.get("_design/sla")
    if ddoc:
        ddoc["views"][topic] = mapreduce
        db.save(ddoc)
    else:
        design = {'views': {topic: mapreduce}}
        db["_design/sla"] = design

    result = db.view('sla/'+ topic, group=True)

    correlation_map = {}
    with open(args.aurin) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for line in result:
                if row[0] == line.key:
                    correlation_map[line.key] = (line.value, row[1])
                    
    correlation_map = sorted(correlation_map.items(), \
    key=(operator.itemgetter(1)), reverse=True)     
    
    populations = list(csv.reader(open("./data/sla_population.csv")))
    populations_dict = {}
    
    for p in populations:
        populations_dict[p[0]] = p[2]
    
    with open('correlation.csv', 'w') as csvfile:   
        csvfile.write('SLA,Tweet Count,Tweets per 1000 Population,Aurin Data\n')    
        for data in correlation_map:        
            csvfile.write('{0},{1},{2},{3}\n'.format(data[0], data[1][0], \
            data[1][0] * 1000 / float(populations_dict.get(data[0], 100000000)), \
            data[1][1]))
    
def main():
    args = parse_args()
    analysis(args)
    
if __name__ == '__main__':
    main()
