import certifi
from pymongo.mongo_client import MongoClient
from airondatarepository import dataconstants

class DataWorker:
    def __init__(self, collection):
        self.client = MongoClient(dataconstants.CONNECTION_STRING, tlsCAFile=certifi.where())
        self.db = self.client[dataconstants.DB_NAME]
        self.collection = self.db[collection]

    def close_connection(self):
        self.client.close()