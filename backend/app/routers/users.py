from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.user import User
from app.schemas.users import UserCreate, UserOut
from app.db import get_db

router = APIRouter(
    prefix= "/users",
    tags= ["users"]
)

#Password Hashing Context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password : str):
    return pwd_context.hash(password)

@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    #Check If Email Already Registered
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email Already Registered")
    
    #Password Hashing
    hashed_password = get_password_hash(user.password)
    
    new_user = User(
        username = user.username,
        email = user.email,
        password_hash = hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user