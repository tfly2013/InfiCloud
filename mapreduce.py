import couchdb

couch = couchdb.Server("http://115.146.94.116:5984/")
db = couch["test"]

mapfun = '''function(doc) {
         emit(doc.id, 1);
}'''

reducefun = "_count"

design = { 'views': {
              'unique': {
                  'map': mapfun,
                  'reduce': reducefun
                }
            } }

ddoc = db["_design/id"]
if ddoc:
    db.delete(ddoc)

db["_design/id"] = design
    
result = db.view('id/unique', group=True)

for row in result:
    print row.key, row.value
