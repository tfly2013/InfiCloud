import couchdb
couch = couchdb.Server("http://115.146.94.116:5984/")
couch.replicate("ssydney","coorsydney", filter = "replicate/by_coordinates")
