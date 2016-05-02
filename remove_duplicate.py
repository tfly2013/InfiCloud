import couchdb

ids = []
couch = couchdb.Server("http://115.146.94.116:5984/")
db = couch["melbourne"]
count = 0
for doc_id in db:
    doc = db[doc_id]
    if doc["id"] in ids:
        db.delete(doc)
        count += 1
    else:
        ids.append(doc["id"])
print(count)
