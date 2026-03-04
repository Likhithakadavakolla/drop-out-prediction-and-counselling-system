import smtplib
from email.message import EmailMessage
import socket

def send_email(to_email, subject, message):
    EMAIL = "likhithakadavakolla@gmail.com"
    PASSWORD = "pnmjaxrnxouwckmj"  # Gmail App Password (spaces removed)

    msg = EmailMessage()
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(message)

    # Set aggressive timeout for faster operation
    socket.setdefaulttimeout(5)
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=5) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)
        print("✅ EMAIL SENT TO:", to_email)
        return True
    except Exception as e:
        print(f"❌ EMAIL FAILED TO: {to_email} - {e}")
        return False
