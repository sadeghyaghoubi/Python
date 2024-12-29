import smtplib
from email.mime.text import MIMEText

EMAIL_ADDRESS = "your email(sender)"
EMAIL_PASSWORD = "APP PASSWORD in your email"
TO_EMAIL = "(reciever email)"

try:
    msg = MIMEText("This is a test email.")
    msg["Subject"] = "Test Email"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
