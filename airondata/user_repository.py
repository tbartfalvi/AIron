import pymongo
import data_constants

# The mongodb user repository
class UserRepository:
    def __init__(self):
        pass

    def insert_user(user):
        client = pymongo.MongoClient(data_constants.CONNECTION_STRING)
        db = client[data_constants.DB_NAME]
        col  = db[data_constants.USER_COLLECTION]
        new_user = col.insert_one(user)
        id = new_user.__inserted_id
        client.close()
        return id
    
    def email_exsits(email: str):
        client = pymongo.MongoClient(data_constants.CONNECTION_STRING)
        db = client[data_constants.DB_NAME]
        col  = db[data_constants.USER_COLLECTION]
        query = { data_constants.EMAIL: email }
        doc = col.find(query)
        for x in doc:
            if x == email:
                return True
            
        return False
    
    def check_user(email: str, password: str):
        pass
