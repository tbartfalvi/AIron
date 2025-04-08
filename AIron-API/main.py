from fastapi import FastAPI, HTTPException
from airondatarepository.datarepository import DataRepository

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/user/{full_name}/{email}/{password}")
def add_user(full_name: str, email: str, password: str):
    repository = DataRepository()
    id = repository.insert_user(full_name, email, password)

    if id is None:
        raise HTTPException(status_code=400, detail="Failed to add new user.")
    
    return { "user_id": str(id) }