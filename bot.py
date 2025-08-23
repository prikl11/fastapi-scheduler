import pytz
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
from telegram import Bot
from database import SessionLocal

from models import Reminder

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)

moscow = pytz.timezone("Europe/Moscow")

def create_reminder(db: Session, user_id: int, telegram_id: int, text: str, remind_at: datetime):
    if remind_at.tzinfo is None:
        remind_at = moscow.localize(remind_at)

    remind_at = remind_at.astimezone(pytz.UTC)
    remind_at = remind_at.replace(tzinfo=None)

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

async def send_reminders():
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        print("Checking reminders at", now)
        reminders = get_due_reminder(db, now)
        for r in reminders:
            print("Sending reminder to", r.telegram_id)
            await bot.send_message(r.telegram_id, r.text)
            mark_done(db, r)
    finally:
        db.close()