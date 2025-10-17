from pydantic import BaseModel, EmailStr

from app.models.user import User

class UserBase(BaseModel):
    username : str
    email : EmailStr
    
class UserCreate(UserBase):
    password : str

class UserOut(UserBase):
    id : int
    
    class Config:
        from_attributes= True
        
class UserResponse(UserBase):
    id: int
    
    class Config:
        orm_mode = True
    