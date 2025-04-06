import dataclasses
import json
from airondatarepository.dataworker import DataWorker
from airondatarepository import dataconstants
from airondatarepository.dataobjects import User
from airondatarepository.encrypt import encrypt_password

# The mongodb data repository
class DataRepository:
    def __init__(self):
        pass

    def insert_user(self, full_name: str, email: str, password: str):
        data_worker = DataWorker(dataconstants.USER_COLLECTION)
        user = User(full_name, email, password, [], [])
        json_string = json.dumps(user, cls=EnhancedJSONEncoder)
        data_dict = json.loads(json_string)
        new_user = data_worker.collection.insert_one(data_dict)
        id = new_user.inserted_id
        data_worker.close_connection()
        return id
    
    def user_exsits(self, email: str):
        data_worker = DataWorker(dataconstants.USER_COLLECTION)
        query = { dataconstants.EMAIL: email }
        doc = data_worker.collection.find(query)
        data_worker.close_connection()
        for x in doc:
            if x.email == email:
                return True
            
        return False
    
    def delete_user(self, email: str):
        data_worker = DataWorker(dataconstants.USER_COLLECTION)
        query = { dataconstants.EMAIL: email }
        result = data_worker.collection.delete_one(query)
        return result.deleted_count > 0
    
    def get_user(self, email: str):
        data_worker = DataWorker(dataconstants.USER_COLLECTION)
        query = { dataconstants.EMAIL: email }
        doc = data_worker.collection.find(query)
        # Wait for connection to check deserialization
        for x in doc:
            return json.load(x)

        return None
    
    def login(self, email: str, password: str):
        data_worker = DataWorker(dataconstants.USER_COLLECTION)
        encrypted_password = encrypt_password(password)
        query = { dataconstants.EMAIL: email, dataconstants.PASSWORD: encrypted_password }
        doc = data_worker.collection.find(query)
        for x in doc:
            return x.id

        return None
    

    
    def test_json(self):
        user = User("Todd Test", "todd@test.com", "access", [], [])
        print(json.dumps(user, cls=EnhancedJSONEncoder))
    
class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)
