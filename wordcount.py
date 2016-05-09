import couchdb
from argparse import ArgumentParser

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

def search(args):
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
        emit(null, 1);
    }'''
    reducefun = "_count"
    mapreduce = {'map': mapfun,'reduce': reducefun}

    ddoc = db.get("_design/count")
    if ddoc:
        ddoc["views"][topic] = mapreduce
        db.save(ddoc)
    else:
        design = {'views': {topic: mapreduce}}
        db["_design/count"] = design

    result = db.view('count/'+ topic, group=True)

    for row in result:
        print row.value

def main():
    args = parse_args()
    print args.topic
    print args.keywords
    search(args)    

if __name__ == '__main__':
    main()
