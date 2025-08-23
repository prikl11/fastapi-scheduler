from datetime import datetime
from fastapi import FastAPI, Depends
from typing import Annotated
from fastapi.openapi.docs import get_swagger_ui_html
from database import get_db, Base, engine
from sqlalchemy.orm import Session
from schemas import UserOut, EventOut, UserCreate, EventCreate, EventUpdate
from crud import create_user, read_users, read_events, read_event, read_user, delete_user, delete_event, update_event, create_event
from models import Event
from export import generate_ics
from fastapi.responses import StreamingResponse
from bot import create_reminder, send_reminders
from apscheduler.schedulers.asyncio import AsyncIOScheduler

app = FastAPI()

scheduler = AsyncIOScheduler()

Base.metadata.create_all(bind=engine)

SessionDep = Annotated[Session, Depends(get_db)]

@app.get("/", include_in_schema=False)
async def root():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="API Docs")

@app.on_event("startup")
def start_scheduler():
    print("Scheduler started")
    scheduler.add_job(send_reminders, "interval", seconds=30)
    scheduler.start()

@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()

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

@app.get("/events.ics")
def export_events(db: SessionDep, user_id: int):
    events = db.query(Event).filter(Event.user_id == user_id).all()
    if not events:
        return {"message": "Events not found"}

    ics_file = generate_ics(events)
    return StreamingResponse(ics_file,
                             media_type="text/calendar",
                             headers={"Content-Disposition": "attachment; filename='events.ics'"})

@app.post("/reminders/")
def create_reminder_route(user_id: int, telegram_id: int, text: str, remind_at: datetime, db: SessionDep):
    return create_reminder(db, user_id, telegram_id, text, remind_at)