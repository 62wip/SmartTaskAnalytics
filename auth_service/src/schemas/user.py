from pydantic import BaseModel, ConfigDict, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
class UserLogin(BaseModel):
    email: EmailStr
    password: str
