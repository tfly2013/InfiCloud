import couchdb, string
from collections import Counter
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
    
    frequent_word_dict = Counter()
    translator = str.maketrans({key: None for key in string.punctuation})
    for doc_id in db:
        doc = db[doc_id]
        for word in doc["text"].translate(translator).split():
            frequent_word_dict[word.lower()] += 1

    Counter(frequent_word_dict).most_common(10)
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