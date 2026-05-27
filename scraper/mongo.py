import pymongo
from scraper.logger import log
from scraper.config import DB_NAME, COLLECTION

def get_mongo_collection(uri):
    client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    db = client[DB_NAME]
    col = db[COLLECTION]
    col.create_index("school_code", unique=True)
    return col