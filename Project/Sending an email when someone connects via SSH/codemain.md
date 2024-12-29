import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import os

LOG_FILE = "/var/log/auth.log"
EMAIL_ADDRESS = "your email (sender)@gmeil.com"
EMAIL_PASSWORD = "qspo wdog qayl fchs"
TO_EMAIL = "mail(reciever email)@gmeil.com"

# تابع برای ارسال ایمیل
def send_email(user, ip, method):
    """ارسال ایمیل برای اطلاع‌رسانی اتصال جدید"""
    try:
        subject = "New SSH Connection Alert"
        body = f"""
        New SSH Connection Detected:

        User: {user}
        IP Address: {ip}
        Authentication Method: {method}

        Please review the connection.
        """
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = TO_EMAIL
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            print(f"Email sent to {TO_EMAIL}: {body}")
    except Exception as e:
        print(f"Error sending email: {e}")
        # ذخیره خطا در فایل لاگ محلی
        with open("/var/log/ssh_monitor_error.log", "a") as error_log:
            error_log.write(f"Error sending email: {str(e)}\n")

# تابع مانیتورینگ فایل لاگ
def monitor_log():
    """مانیتور فایل لاگ برای شناسایی اتصالات جدید"""
    print("Monitoring log file for new connections...")

    # بررسی دسترسی به فایل لاگ
    if not os.path.exists(LOG_FILE):
        print(f"Log file {LOG_FILE} does not exist.")
        return
    elif not os.access(LOG_FILE, os.R_OK):
        print(f"Log file {LOG_FILE} is not readable.")
        return
    else:
        print(f"Log file {LOG_FILE} is accessible.")

    with open(LOG_FILE, "r") as file:
        # انتقال به انتهای فایل
        file.seek(0, os.SEEK_END)

        while True:
            line = file.readline()
            if not line:
                time.sleep(1)
                continue
            print(f"Log detected: {line.strip()}")
            if "Accepted password" in line:
                parts = line.split()
                user = parts[8]
                ip = parts[10]
                method = "password"
                print(f"User: {user}, IP: {ip}, Method: {method}")
                send_email(user, ip, method)
                time.sleep(2)  # جلوگیری از ارسال سریع ایمیل‌ها
            elif "Accepted publickey" in line:
                parts = line.split()
                user = parts[8]
                ip = parts[10]
                method = "publickey"
                print(f"User: {user}, IP: {ip}, Method: {method}")
                send_email(user, ip, method)
                time.sleep(2)  # جلوگیری از ارسال سریع ایمیل‌ها

# اجرای کد اصلی
if __name__ == "__main__":
    try:
        monitor_log()
    except Exception as e:
        print(f"Unexpected error: {e}")
        with open("/var/log/ssh_monitor_error.log", "a") as error_log:
            error_log.write(f"Unexpected error: {str(e)}\n")
