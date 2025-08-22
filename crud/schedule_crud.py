from sqlalchemy.orm import Session
from models import Event
from schemas import EventCreate, EventUpdate
from fastapi import HTTPException

def create_event(db: Session, event: EventCreate):
    existing_event = db.query(Event).filter(Event.title == event.title,
                                            Event.start_time == event.started_at,
                                            Event.end_time == event.ended_at).first()
    if existing_event:
        raise HTTPException(status_code=409, detail="Event already exists")

    new_event = Event(title=event.title, start_time=event.started_at, end_time=event.ended_at, user_id=event.user_id)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

def read_event(db: Session, event_id: int):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return event

def read_events(db: Session):
    events = db.query(Event).all()
    if not events:
        return {"message": "No events found"}

    return events

def update_event(db: Session, event: EventUpdate):
    existing_event = db.query(Event).filter(Event.id == event.id).first()
    if not existing_event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.title is not None:
        existing_event.title = event.title
    if event.start_time is not None:
        existing_event.start_time = event.start_time
    if event.end_time is not None:
        existing_event.end_time = event.end_time
    if event.user_id is not None:
        existing_event.user_id = event.user_id

    db.commit()
    db.refresh(existing_event)
    return existing_event

def delete_event(db: Session, event_id: int):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(event)
    db.commit()
    return {"message": "Event deleted"}