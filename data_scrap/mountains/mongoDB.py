from pymongo import MongoClient

db_url = "mongodb://127.0.0.1:27017/"

def DBinsert(db, data):

    db_name = db['db_name']
    collection_name = db['collection_name']

    with MongoClient(db_url) as client:
        db = client[db_name]
        if (collection_name not in db.list_collection_names()):
            db.create_collection(collection_name)

        result = db[collection_name].insert_one(data)
        print(result.inserted_id)


def DBfindAll(db):

    db_name = db['db_name']
    collection_name = db['collection_name']

    with MongoClient(db_url) as client:
        db = client[db_name]
        result = db[collection_name].find({}, {'_id':0})

    return result

# DBfind(db, {'_id':0, 'name':1, 'site':1})
def DBfind(db, keys):

    db_name = db['db_name']
    collection_name = db['collection_name']

    with MongoClient(db_url) as client:
        db = client[db_name]
        result = db[collection_name].find({}, keys)

    return result


