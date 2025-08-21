from datetime import datetime
from pydantic import BaseModel

class EventCreate(BaseModel):
    title: str
    started_at: datetime
    ended_at: datetime
    user_id: int

class EventOut(EventCreate):
    id: int

    class Config:
        from_attributes = True

class EventUpdate(BaseModel):
    title: str | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None
    user_id: int | None = None