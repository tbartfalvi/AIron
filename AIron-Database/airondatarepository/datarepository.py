import dataclasses
import json
from airondatarepository.dataworker import DataWorker
from airondatarepository import dataconstants
from airondatarepository.dataobjects import User
from airondatarepository.encrypt import encrypt_password
from airondatarepository.encrypt import check_password
from bson import ObjectId

# The mongodb data repository
class DataRepository:
    def __init__(self):
        pass

    def insert_user(self, full_name: str, email: str, password: str):
        encryoted_password = encrypt_password(password)
        data_worker = DataWorker(dataconstants.USER_COLLECTION)
        user = User(full_name, email, encryoted_password, [], [])
        json_string = json.dumps(user, cls=EnhancedJSONEncoder)
        data_dict = json.loads(json_string)
        new_user = data_worker.collection.insert_one(data_dict)
        id = new_user.inserted_id
        data_worker.close_connection()
        return id
    
    def user_exsits(self, id: str):
        exists = False
        data_worker = DataWorker(dataconstants.USER_COLLECTION)
        query = { dataconstants.ID: ObjectId(id) }
        doc = data_worker.collection.find_one(query)
        
        if doc:
            exists = True

        data_worker.close_connection()

        return exists
    
    def delete_user(self, id: str):
        data_worker = DataWorker(dataconstants.USER_COLLECTION)
        query = { dataconstants.ID: id }
        result = data_worker.collection.delete_one(query)

        data_worker.close_connection()

        return result.deleted_count > 0
    
    def get_user(self, id: str):
        result = None
        data_worker = DataWorker(dataconstants.USER_COLLECTION)
        query = { dataconstants.ID: ObjectId(id) }
        doc = data_worker.collection.find_one(query)
  
        if doc:
            result = User(
                doc[dataconstants.FULL_NAME], 
                doc[dataconstants.EMAIL], 
                doc[dataconstants.PASSWORD],
                doc[dataconstants.INPUTS], 
                doc[dataconstants.SCHEDULES])
            
        data_worker.close_connection()

        return result
    
    def login(self, email: str, password: str):
        result = None
        data_worker = DataWorker(dataconstants.USER_COLLECTION)
        query = { dataconstants.EMAIL: email }
        doc = data_worker.collection.find_one(query)
        
        if doc and check_password(password, doc[dataconstants.PASSWORD]):
            result = doc[dataconstants.ID]

        data_worker.close_connection()
        
        return result

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)