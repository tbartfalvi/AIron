import dataclasses
from fastapi import FastAPI, HTTPException
from airondatarepository.datarepository import DataRepository
from models import User
import json
from airondatarepository.dataenums import ScheduleType

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/user/{full_name}/{email}/{password}")
def add_user(full_name: str, email: str, password: str):
    repository = DataRepository()

    exists = repository.user_exsits(email)
    
    if exists:
        raise HTTPException(status_code=401, detail="User already exists in the system.")

    id = repository.insert_user(full_name, email, password)

    if id is None:
        raise HTTPException(status_code=402, detail="Failed to add new user.")
    
    return { "user_id": str(id) }

@app.post("/login/{email}/{password}")
def login(email: str, password: str):
    repository = DataRepository()
    result = repository.login(email, password)
    return { "result": str(result) }

@app.post("/user-info/{id}")
def get_user(id: str):
    repository = DataRepository()
    result = repository.get_user(id)
 
    if result == None:
        raise HTTPException(status_code=403, detail="User not found.")
    
    user = User(id, result.full_name, result.email)
    user_json = json.dumps(user, cls=EnhancedJSONEncoder)
    return { "user": user_json }

@app.post("/schedule/{user_id}/{name}/{type}/{schedule_json}")
def add_schedule(user_id: str, name: str, type: int, schedule_json: str):
    repository = DataRepository()
    result = repository.add_schedule(user_id, name, ScheduleType(type), schedule_json)
    return { "result": str(result) }

@app.post("/schedules/{user_id}")
def get_schedules(user_id: str):
    repository = DataRepository()
    result = repository.get_schedules_by_user(user_id)
    return { "schedules": result }

@app.post("/schedule-get/{user_id}/{scehdule_id}")
def get_schedule_by_id(user_id: str, schedule_id: str):
    repository = DataRepository()
    result = repository.get_schdule_by_id(user_id, schedule_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Schedule not found.")

    return { "schedule": result }

@app.delete("/schedule-delete/{user_id}/{schedule_id}")
def delete_schedule(user_id: str, schedule_id: str):
    repository = DataRepository()
    result = repository.delete_schedule(user_id, schedule_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Failed to delete schedule.")
    
    return { "result": str(result) }

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)
