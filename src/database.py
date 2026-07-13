import pymongo
import config

mongo_client = pymongo.MongoClient(config.MONGO_URL)
db = mongo_client[config.db_name]

def get_data_collection():
    data_collection = db[config.collection_data]
    return data_collection