import dataclasses
import json
import uuid
from airondatarepository.dataworker import DataWorker
from airondatarepository import dataconstants
from airondatarepository.dataobjects import User
from airondatarepository.encrypt import encrypt_password
from airondatarepository.encrypt import check_password
from airondatarepository.dataobjects import Schedule
from airondatarepository.dataenums import ScheduleType
from bson import ObjectId
from datetime import datetime

# The mongodb data repository
class DataRepository:
    def __init__(self):
        pass

    # User functions
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
    
    def user_exsits(self, email: str):
        exists = False
        data_worker = DataWorker(dataconstants.USER_COLLECTION)
        query = { dataconstants.EMAIL: email }
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
    
    def add_schedule(self, id: str, name: str, type: ScheduleType, schedudle_json: str):
        user = self.get_user(id)
    
        if user:
            # Generate a default CSV with 5 empty columns
            default_csv = ",,,,"
    
            schedule = Schedule(
                str(uuid.uuid4()),
                name,
                str(type),
                schedudle_json,
                default_csv,
                datetime.fromisoformat(datetime.now().isoformat()).__str__()
            )
    
            user.schedules.append(schedule)
            data_worker = DataWorker(dataconstants.USER_COLLECTION)
            query = { dataconstants.ID: ObjectId(id) }
            json_string = json.dumps(user, cls=EnhancedJSONEncoder)
            data_dict = json.loads(json_string)
            result = data_worker.collection.update_one(query, { "$set": data_dict})
    
            data_worker.close_connection()
    
            return result.modified_count == 1
    
        return False
    
    def get_schedules_by_user(self, id: str):
        user = self.get_user(id)
        if user:
            return user.schedules
        
        return []

    def delete_schedule(self, user_id: str, schedule_id: str) -> bool:
        """
        Atomically remove a schedule from the user's `schedules` array.
        Returns True if a document was modified, False otherwise.
        """
        _id         = ObjectId(user_id) if len(user_id) == 24 else user_id
        data_worker = DataWorker(dataconstants.USER_COLLECTION)
        res         = data_worker.collection.update_one(
            {"_id": _id, "schedules.id": schedule_id},
            {"$pull": {"schedules": {"id": schedule_id}}},
        )
        data_worker.close_connection()
        return res.modified_count > 0
    
    def get_schdule_by_id(self, user_id: str, schedule_id: str):
        try:
            schedules = self.get_schedules_by_user(user_id)
            for sched in schedules:
                if sched.get("id") == schedule_id:
                    return sched   # Return the complete schedule object.
            raise Exception(f"Schedule with id {schedule_id} not found.")
        except Exception as e:
            print("Error in get_schdule_by_id:", str(e))
            raise





class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)
