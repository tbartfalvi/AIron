import dataclasses
import sys, os, io, json
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from airondatarepository.datarepository import DataRepository
from airondatarepository.dataenums import ScheduleType

sys.path.append(os.path.dirname(__file__))
from models import User   # keep after sys.path append


# ───────────────────────────────────────────────────────────────
# FastAPI boilerplate
# ───────────────────────────────────────────────────────────────
app = FastAPI(docs_url="/documentation", redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ───────────────────────────────────────────────────────────────
# Helpers
# ───────────────────────────────────────────────────────────────
def _to_dict(s: Any) -> dict:
    """Return a plain dict representation of a schedule."""
    if isinstance(s, dict):
        return s
    if dataclasses.is_dataclass(s):
        return dataclasses.asdict(s)
    raise TypeError("schedule must be dict or dataclass")


# ───────────────────────────────────────────────────────────────
# Routes
# ───────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "Hello World"}


# ---------- User ----------
@app.post("/user/{full_name}/{email}/{password}")
async def add_user(full_name: str, email: str, password: str):
    repo = DataRepository()
    if repo.user_exsits(email):
        raise HTTPException(status_code=401, detail="User already exists")

    user_id = repo.insert_user(full_name, email, password)
    if not user_id:
        raise HTTPException(status_code=500, detail="Failed to add user")
    return {"user_id": str(user_id)}


@app.post("/login/{email}/{password}")
async def login(email: str, password: str):
    repo = DataRepository()
    result = repo.login(email, password)
    return {"result": str(result)}


@app.get("/user-info/{user_id}")
async def get_user(user_id: str):
    repo = DataRepository()
    u = repo.get_user(user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": json.dumps(User(user_id, u.full_name, u.email), cls=EnhancedJSONEncoder)}


# ---------- Schedule CRUD ----------
@app.post("/schedule/{user_id}/{name}/{stype}/{schedule_json}")
async def add_schedule(user_id: str, name: str, stype: int, schedule_json: str):
    repo = DataRepository()
    ok = repo.add_schedule(user_id, name, ScheduleType(stype), schedule_json)
    return {"result": str(ok)}


@app.get("/schedules/{user_id}")
async def get_schedules(user_id: str):
    repo = DataRepository()
    return {"schedules": repo.get_schedules_by_user(user_id)}


@app.api_route("/schedule-get/{user_id}/{schedule_id}", methods=["GET", "POST"])
async def get_schedule_by_id(user_id: str, schedule_id: str):
    repo = DataRepository()
    sched = repo.get_schdule_by_id(user_id, schedule_id)
    if not sched:
        raise HTTPException(status_code=404, detail="Schedule not found")

    sched = _to_dict(sched)   # ensure dict
    return {
        "id":      sched["id"],
        "name":    sched["name"],
        "json":    sched["json"],
        "csv":     sched["csv"],
        "type":    sched["type"],
        "created": sched["created_on"],
    }


@app.post("/schedule-delete/{user_id}/{schedule_id}")
async def delete_schedule(user_id: str, schedule_id: str):
    print("main.py: delete_schedule: open data repository.")
    repo = DataRepository()
    print("main.py: calling delete_schedule function")
    ok = repo.delete_schedule(user_id, schedule_id)
    if not ok:
        raise HTTPException(status_code=404, detail="main.py: Delete failed")
    
    print("main.py: successfully called delete_schedule!")
    return {"result": "True"}


@app.get("/schedule-download/{user_id}/{schedule_id}")
async def download_schedule_csv(user_id: str, schedule_id: str):
    repo = DataRepository()
    sched = repo.get_schdule_by_id(user_id, schedule_id)
    if not sched:
        raise HTTPException(status_code=404, detail="Schedule not found")

    sched   = _to_dict(sched)
    csv_str = sched.get("csv") or "Program Name,Exercise,Sets,Reps,Weight"
    buffer  = io.BytesIO(csv_str.encode("utf-8"))

    filename = f"{sched.get('name', 'workout')}.csv"
    headers  = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return StreamingResponse(buffer, media_type="text/csv", headers=headers)


# ---------- JSON encoder ----------
class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


# ---------- Local dev ----------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
