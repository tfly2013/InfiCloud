import couchdb, string
import csv
import operator
from collections import Counter
from argparse import ArgumentParser
from location import *

def parse_args():
    """ Read arguments from command line."""

    parser = ArgumentParser(
        description="Twitter harvesting application."
    )
    parser.add_argument(
        '--dbname',
        type=str,
        help='Name of CouchDB database to insert data into.'
    )
    parser.add_argument(
        '--aurin',
        type=str,
        default="perth",
        help='Database name for search.' 
    )    
    return parser.parse_args()


    
def analysis(args):
    # Set up couch db
    couch = couchdb.Server("http://115.146.94.116:5984/")
    db = couch[args.dbname]
    

    
#    topic = "test"
#    reducefun = "_count"
#    mapreduce = {'map': map_fun,'reduce': reducefun}
#
#    ddoc = db.get("_design/test")
#    if ddoc:
#        ddoc["views"][topic] = mapreduce
#        db.save(ddoc)
#    else:
#        design = {'views': {topic: mapreduce}}
#        db["_design/test"] = design
#
#    result = db.view('test/'+ topic, group=True)
    map_fun = '''function(doc) {
       if (doc.coordinates != null) {
           emit(doc.coordinates, doc.text);
       }
    }'''
    
    results = db.query(map_fun)
    sla = Counter()
    keyword = "bored"
    for row in results:
        if keyword in row.value.lower():
            sla[find_sla(row.key["coordinates"][0], row.key["coordinates"][1])] +=1
    print ("keyword = " + keyword)
    #print (sla)
    
    correlation_map = {}
    with open(args.aurin) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for key in sla.elements():
                if row[0] == key:
                    correlation_map[key] = (sla[key], row[1])
                    
#    correlation_map = [(v, k) for k, v in correlation_map.items()]
#    correlation_map.sort()
#    correlation_map.reverse()             # so largest is first
#    correlation_map = [(k, v) for v, k in items]
                    
    correlation_map = sorted(correlation_map.items(), key=(operator.itemgetter(1)), reverse=True)               
    print (correlation_map)        
            
    
        

#    for row in result:
#        print(row.value)
#        print(row.key)
#    frequent_word_dict = Counter()
#    translator = str.maketrans({key: None for key in string.punctuation})
#    for doc_id in db:
#        doc = db[doc_id]
#        for word in doc["text"].translate(translator).split():
#            frequent_word_dict[word.lower()] += 1
#
#    Counter(frequent_word_dict).most_common(10)
#    retrieve_mapfn = """function(doc)
#                        {
#                          if (doc.palce != null) {
#                            emit(doc, null);
#                          }
#                        }"""
#                        
#    for row in db.query(retrieve_mapfn):
#        print (row.key)
#    design = { 'views': 
#                 {
#                 'all_tweets': {
#                        'map': retrieve_mapfn
#                               }
#                 } 
#             }
#    db["_design/all_tweets"] = design
    
def main():
    args = parse_args()
    analysis(args)
    
if __name__ == '__main__':
    main()
