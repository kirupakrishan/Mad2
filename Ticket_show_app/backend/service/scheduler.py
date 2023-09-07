import schedule
from routes import app
import time
from Models.ticket_model import Ticket
from Models.venue_model import Venue
from Models.user_model import Users
from Models.show_model import Show
from datetime import datetime, timedelta
from email.message import EmailMessage
import smtplib
import ssl
from dotenv import load_dotenv
import os

load_dotenv()
email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")


previous_day_5pm = datetime.now().replace(hour=17, minute=0, second=0,
                                          microsecond=0) - timedelta(days=1)
today_5pm = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)

def send_email(email, subject, message):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = str(email)
    msg.set_content(message)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_address, email_password)
        server.send_message(msg)


def dailyReport():
    with app.app_context():
        users = Users.query.all()
        for user in users:
            username = user.name
            email = user.email
            tickets = Ticket.query.filter_by(user_id=user.id).all()
            total_booking = 0
            if datetime.now().day == 1:
                monthlyReport()
                continue
            for ticket in tickets:
                booked_on = ticket.created_at
                if previous_day_5pm <= booked_on <= today_5pm:
                    total_booking += 1

            body = f"Hi {username},\n\nYou have {total_booking} tickets today.\n\nRegards,\nTeam MovieX"
            print(body)
            # send_mail(email, "Daily Report", body)
            send_email(email, "Daily Report", body)
            print("Mail Sent")

def monthlyReport():
    with app.app_context():
        users = Users.query.all()
        now = datetime.now()
        for user in users:
            username = user.username
            email = user.email
            tickets = Ticket.query.filter_by(user_id=user.id).all()
            total_booking = 0
            for ticket in tickets:
                booked_on = ticket.created_at
                if now.year == booked_on.year and now.month == booked_on.month:
                    total_booking += 1
            body = f"Hi {username},\n\nYou have {total_booking} tickets booked this month.\n\nRegards,\nTeam MovieX"
            send_email(email, "Monthly Report", body)
            print("Mail Sent")

def Scheduled():
    schedule.every().day.at("22:06").do(dailyReport)

    while True:
        schedule.run_pending()
        time.sleep(1)
