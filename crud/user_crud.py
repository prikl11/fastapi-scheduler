from sqlalchemy.orm import Session
from schemas import UserCreate
from models import User
from fastapi import HTTPException
from auth import hash_password

def create_user(db: Session, user: UserCreate):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(409, "User already exists")

    new_user = User(email=user.email, username=user.username, password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def read_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User does not exist")

    return user

def read_users(db: Session):
    users = db.query(User).all()
    if not users:
        return {"message": "No users found"}

    return users

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User does not exist")

    db.delete(user)
    db.commit()
    return {"message": "User deleted"}