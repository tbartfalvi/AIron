import dataclasses
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from airondatarepository.datarepository import DataRepository
import sys, os, io
sys.path.append(os.path.dirname(__file__))
from models import User
import json
from airondatarepository.dataenums import ScheduleType
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(docs_url="/documentation", redoc_url=None)

origins = ["*"]  # Allows all origins.  Remove for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/user/{full_name}/{email}/{password}")
async def add_user(full_name: str, email: str, password: str):
    repository = DataRepository()

    exists = repository.user_exsits(email)
    
    if exists:
        raise HTTPException(status_code=401, detail="User already exists in the system.")

    id = repository.insert_user(full_name, email, password)

    if id is None:
        raise HTTPException(status_code=402, detail="Failed to add new user.")
    
    return { "user_id": str(id) }

@app.post("/login/{email}/{password}")
async def login(email: str, password: str):
    repository = DataRepository()
    result = repository.login(email, password)
    return { "result": str(result) }

@app.get("/user-info/{id}")
async def get_user(id: str):
    repository = DataRepository()
    result = repository.get_user(id)
 
    if result == None:
        raise HTTPException(status_code=403, detail="User not found.")
    
    user = User(id, result.full_name, result.email)
    user_json = json.dumps(user, cls=EnhancedJSONEncoder)
    return { "user": user_json }

@app.post("/schedule/{user_id}/{name}/{type}/{schedule_json}")
async def add_schedule(user_id: str, name: str, type: int, schedule_json: str):
    repository = DataRepository()
    result = repository.add_schedule(user_id, name, ScheduleType(type), schedule_json)
    return { "result": str(result) }

@app.get("/schedules/{user_id}")
async def get_schedules(user_id: str):
    repository = DataRepository()
    result = repository.get_schedules_by_user(user_id)
    return { "schedules": result }

@app.api_route("/schedule-get/{user_id}/{schedule_id}", methods=["GET", "POST"])
async def get_schedule_by_id(user_id: str, schedule_id: str):
    repository = DataRepository()
    schedule = repository.get_schdule_by_id(user_id, schedule_id)
    
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found.")
    
    return {
        "id":        schedule.get("id"),
        "name":      schedule.get("name"),
        "json":      schedule.get("json"),
        "csv":       schedule.get("csv"),
        "type":      schedule.get("type"),
        "created":   schedule.get("created_on")
    }


@app.delete("/schedule-delete/{user_id}/{schedule_id}")
async def delete_schedule(user_id: str, schedule_id: str):
    """
    Delete a schedule by its ID.
    Enhanced with better error handling and validation.
    """
    print(f"API: Delete request received for schedule {schedule_id}, user {user_id}")
    
    # Validate inputs
    if not user_id or not schedule_id:
        print(f"API: Invalid inputs - user_id: '{user_id}', schedule_id: '{schedule_id}'")
        raise HTTPException(status_code=400, detail="Invalid user ID or schedule ID")
    
    try:
        # Process deletion
        repository = DataRepository()
        result = repository.delete_schedule(user_id, schedule_id)
        
        print(f"API: Delete operation result: {result}")
        
        # Handle success/failure
        if not result:
            print(f"API: Delete operation failed for schedule {schedule_id}")
            raise HTTPException(status_code=404, detail=f"Failed to delete schedule with ID {schedule_id}")
        
        print(f"API: Successfully deleted schedule {schedule_id}")
        return { "result": "True" }  # Return string "True" to match expected frontend value
        
    except Exception as e:
        print(f"API: Error in delete_schedule endpoint: {str(e)}")
        # Return a 500 error for unexpected exceptions
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.get("/schedule-download/{user_id}/{schedule_id}")
async def download_schedule_csv(user_id: str, schedule_id: str):
    repo      = DataRepository()
    schedule  = repo.get_schdule_by_id(user_id, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    csv_str = schedule.get("csv") or "Program Name,Exercise,Sets,Reps,Weight"
    buffer  = io.BytesIO(csv_str.encode("utf-8"))
    filename = f"{schedule.get('name','workout')}.csv"
    headers  = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return StreamingResponse(buffer, media_type="text/csv", headers=headers)

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
