import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import os

def send_email(to_email, subject, body, smtp_config):
    """
    Sends an email using SMTP.
    """
    if not to_email:
        print("No email provided, skipping...")
        return False

    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_config['user']
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(smtp_config['server'], smtp_config['port'])
        server.starttls()
        server.login(smtp_config['user'], smtp_config['password'])
        server.send_message(msg)
        server.quit()
        print(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        return False

def send_telegram_alert(message, bot_token, chat_id):
    """
    Sends an alert to a Telegram bot.
    """
    if not bot_token or not chat_id:
        print("Telegram config missing, skipping alert...")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Telegram alert sent successfully.")
            return True
        else:
            print(f"Failed to send Telegram alert: {response.text}")
            return False
    except Exception as e:
        print(f"Error sending Telegram alert: {e}")
        return False

if __name__ == "__main__":
    # Test (will fail without real credentials, but checks logic)
    print("Testing outreach module (logic check)...")
    # send_email("test@example.com", "Hello", "This is a test", {})
