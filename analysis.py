import couchdb, string
from argparse import ArgumentParser

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
    return parser.parse_args()


    
def analysis(args):
    # Set up couch db
    couch = couchdb.Server("http://115.146.94.116:5984/")
    db = couch[args.dbname]
    
    frequent_word_dict = {}
    for doc_id in db:
        doc = db[doc_id]
        for word in doc["text"].translate(string.maketrans("",""), string.punctuation).split():
            if word not in frequent_word_dict:
                frequent_word_dict[word] = 1
            else:
                frequent_word_dict[word] = frequent_word_dict[word] + 1
    
    items = [(v, k) for k, v in frequent_word_dict.items()]
    items.sort()
    items.reverse()             # so largest is first
    items = [(k, v) for v, k in items]
    
    for i in range(10):
        print (items[i])
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