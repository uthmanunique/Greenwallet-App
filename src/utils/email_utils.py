import smtplib
import random
import os
from email.message import EmailMessage

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
GMAIL_USER = os.getenv("GMAIL_USER")  # Set this in .env
GMAIL_PASS = os.getenv("GMAIL_PASS")

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email: str, otp: str):
    msg = EmailMessage()
    msg["Subject"] = "Your GreenWallet OTP Code"
    msg["From"] = GMAIL_USER
    msg["To"] = email
    msg.set_content(f"Your OTP code is {otp}. It expires in 10 minutes.")

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        server.send_message(msg)
