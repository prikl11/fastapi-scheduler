from database import Base
from sqlalchemy import Integer, Text, String, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    username = Column(String(50), index=True)
    password = Column(Text, index=True)

    events = relationship("Event", back_populates="user")

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(30), index=True)
    start_time = Column(DateTime, index=True)
    end_time = Column(DateTime, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="events")