from datetime import datetime
from pydantic import BaseModel

class EventCreate(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime
    user_id: int

class EventOut(EventCreate):
    id: int

    class Config:
        from_attributes = True

class EventUpdate(BaseModel):
    id: int
    title: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    user_id: int | None = None