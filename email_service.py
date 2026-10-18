import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    def __init__(self):
        self.host = os.getenv("EMAIL_HOST", "smtp.gmail.com")
        self.port = int(os.getenv("EMAIL_PORT", 587))
        self.user = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_PASS")

    def send_email(self, to_email, subject, body, is_html=False):
        if not self.user or not self.password:
            print("Email credentials not found in .env")
            return False

        message = MIMEMultipart()
        message["From"] = self.user
        message["To"] = to_email
        message["Subject"] = subject

        if is_html:
            message.attach(MIMEText(body, "html"))
        else:
            message.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.send_message(message)
            print(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

if __name__ == "__main__":
    # Test (requires valid .env)
    service = EmailService()
    # service.send_email("test@example.com", "Test Subject", "Test Body")
