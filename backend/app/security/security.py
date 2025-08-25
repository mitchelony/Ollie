from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from pydantic import BaseModel
from app.db import get_db
from app.security.password_utils import verify_password
from app.security.token_utils import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
    )

class LoginRequest(BaseModel):
    username: str
    password: str
    
@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
<<<<<<< HEAD
    if not user or not verify_password(request.password, user.User.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    
    access_token = create_access_token({"sub": user.username})
=======
    if not user or not verify_password(request.password, getattr(user, "hashed_password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
        )
    
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
>>>>>>> wip/save-local
