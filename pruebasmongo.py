import pymongo

myclient = pymongo.MongoClient("mongodb://localhost")

print(myclient.list_database_names())
