from sqlalchemy.orm import Session
from datetime import datetime
import os
from dotenv import load_dotenv
from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler
from database import SessionLocal

from models import Reminder

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)

def create_reminder(db: Session, user_id: int, telegram_id: int, text: str, remind_at: datetime):
    reminder = Reminder(user_id=user_id, telegram_id=telegram_id, text=text, remind_at=remind_at)
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder

def get_due_reminder(db: Session, now: datetime):
    return db.query(Reminder).filter(Reminder.remind_at <= now, Reminder.done == False).all()

def mark_done(db: Session, reminder: Reminder):
    reminder.done = True
    db.commit()

def send_reminders():
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        print("Checking reminders at", now)
        reminders = get_due_reminder(db, now)
        for r in reminders:
            print("Sending reminder to", r.telegram_id)
            bot.send_message(r.telegram_id, r.text)
            mark_done(db, r)
    finally:
        db.close()