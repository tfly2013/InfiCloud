"""
Team: Cluster and Cloud Computing Team 3
Contents: Assigment 2
Authors: Kimple Ke, Roger Li, Fei Tang, Bofan Jin, David Ye
"""
import couchdb
from argparse import ArgumentParser

def parse_args():
    """ Read arguments from command line."""

    parser = ArgumentParser(
        description="CouchDB database duplicate ID removal application."
    )
    parser.add_argument(
        '--index',
        type=int,
        default=0,
        help='Index of virtual machine'
    )
    return parser.parse_args()

def remove_duplicate(dbname):
	""" Remove duplicate IDs in given database."""
	# a set contains all tweet IDs that exist
	ids = set()
	# connect to couchDB
	couch = couchdb.Server("http://115.146.94.116:5984/")
	db = couch[dbname]
	for doc_id in db:
	  doc = db[doc_id]
	  # retrieve ID of tweet
	  id = doc["id"]
	  # delete tweets if its already in db
	  if id in ids:
	    db.delete(doc)
	  else:
	    ids.add(id)

def main():
    args = parse_args()
    remove_duplicate(args.db)


if __name__ == '__main__':
    main()
