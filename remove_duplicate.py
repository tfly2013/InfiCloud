import couchdb

ids = set()
couch = couchdb.Server("http://115.146.94.116:5984/")
db = couch["melbourne"]
for doc_id in db:
    doc = db[doc_id]
	id = doc["id"]
    if id in ids:
        db.delete(doc)
    else:
        ids.add(id)
