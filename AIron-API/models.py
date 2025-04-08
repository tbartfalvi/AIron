from pydantic import BaseModel

class UserPayload(BaseModel):
    full_name: str
    email: str
    password: str
