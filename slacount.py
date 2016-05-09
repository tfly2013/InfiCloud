import couchdb, string
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
        default="perth",
        help='Database name for search.' 
    )
    parser.add_argument(
        '--keywords',
        type=str,
        nargs='+',
        help='Keywords for search.'        
    )
    return parser.parse_args()

def sla_search(args):
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
    if (doc.text.search(re) != -1 && doc.coordinates != null)
        emit(doc.coordinates, 1);
    }'''

    option = {'map': mapfun}
    
    ddoc = db.get("_design/sla")
    if ddoc:
        ddoc["views"][topic] = option
        db.save(ddoc)
    else:
        design = {'views': {topic: option}}
        db["_design/sla"] = design

    result = db.view('sla/'+ topic)

    sla = Counter()
        
    for row in result:        
        sla[find_sla(row.key["coordinates"][0], row.key["coordinates"][1])] +=1
    print sla
    
#    correlation_map = {}
#    with open(args.aurin) as csvfile:
#        reader = csv.reader(csvfile)
#        for row in reader:
#            for key in sla.elements():
#                if row[0] == key:
#                    correlation_map[key] = (sla[key], row[1])
#                    
#    correlation_map = [(v, k) for k, v in correlation_map.items()]
#    correlation_map.sort()
#    correlation_map.reverse()             # so largest is first
#    correlation_map = [(k, v) for v, k in items]
                    
    correlation_map = sorted(correlation_map.items(), key=(operator.itemgetter(1)), reverse=True)               
    print (correlation_map) 
    
def main():
    args = parse_args()
    sla_search(args)
    
if __name__ == '__main__':
    main()
