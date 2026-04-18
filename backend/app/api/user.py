from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.api.user_deps import get_current_user
from app.schemas.user import UserRegister, UserLogin, Token, UserResponse
from app.services.user import register_user, login_user
from app.models.user import User
from app.core.security import create_access_token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    user = register_user(
        db,
        username=user_data.username,
        password=user_data.password
    )
    
    # Create token after registration
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"user_id": user.id, "username": user.username},  
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username  
    }

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user, access_token = login_user(
        db,
        username=user_data.username,  
        password=user_data.password
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username  
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    return {"message": "Logged out successfully"}