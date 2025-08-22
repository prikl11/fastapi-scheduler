from fastapi import FastAPI, Depends
from typing import Annotated
from database import get_db, Base, engine
from sqlalchemy.orm import Session
from schemas import UserOut, EventOut, UserCreate, EventCreate, EventUpdate
from crud import create_user, read_users, read_events, read_event, read_user, delete_user, delete_event, update_event, create_event

app = FastAPI()

Base.metadata.create_all(bind=engine)

SessionDep = Annotated[Session, Depends(get_db)]

@app.get("/")
def read_root():
    return {"message:" "FastAPI is working!"}

@app.post("/users/", response_model=UserOut)
def create_user_route(db: SessionDep, user: UserCreate):
    return create_user(db, user)

@app.get("/users/{user_id}", response_model=UserOut)
def read_user_route(db: SessionDep, user_id: int):
    return read_user(db, user_id)

@app.get("/users/", response_model=list[UserOut])
def read_users_route(db: SessionDep):
    return read_users(db)

@app.delete("/users/{user_id}")
def delete_user_route(db: SessionDep, user_id: int):
    return delete_user(db, user_id)

@app.post("/events/", response_model=EventOut)
def create_event_route(db: SessionDep, event: EventCreate):
    return create_event(db, event)

@app.get("/events/{event_id}", response_model=EventOut)
def read_event_route(db: SessionDep, event_id: int):
    return read_event(db, event_id)

@app.get("/events/", response_model=list[EventOut])
def read_events_route(db: SessionDep):
    return read_events(db)

@app.patch("/events/{event_id}", response_model=EventOut)
def update_event_route(db: SessionDep, event: EventUpdate):
    return update_event(db, event)

@app.delete("/events/{event_id}")
def delete_event_route(db: SessionDep, event_id: int):
    return delete_event(db, event_id)