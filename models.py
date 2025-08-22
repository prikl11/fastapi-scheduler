from database import Base
from sqlalchemy import Integer, Text, String, Column, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    username = Column(String(50), index=True)
    password = Column(Text, index=True)

    events = relationship("Event", back_populates="user")
    reminders = relationship("Reminder", back_populates="user")

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(30), index=True)
    start_time = Column(DateTime, index=True)
    end_time = Column(DateTime, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    user = relationship("User", back_populates="events")

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    telegram_id = Column(Integer, index=True)
    text = Column(String(200), index=True)
    remind_at = Column(DateTime, index=True)
    done = Column(Boolean, index=True, default=False)

    user = relationship("User", back_populates="reminders")