"""
Email Dispatcher Module for Mukund Pratap Srivastav's Portfolio
Handles direct SMTP dispatch and fallback Gmail Web Compose links.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# Load configuration from environment or .env file
def load_env_file():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k.strip(), v.strip())

load_env_file()

SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SENDER_EMAIL = os.environ.get('SMTP_USER', '')
SENDER_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD', '') # 16-character Google App Password
RECIPIENT_EMAIL = os.environ.get('NOTIFICATION_EMAIL', 'mukund.tech.dev@gmail.com')

def generate_gmail_compose_url(sender_name, sender_email, subject, message):
    """Generates a direct Gmail Web Compose URL pre-filled with the message."""
    import urllib.parse
    su = f"Portfolio Inquiry: {subject or 'New Project'} (from {sender_name})"
    body = f"Hello Mukund Pratap Srivastav,\n\nYou received a new message from your portfolio website:\n\n" \
           f"Name: {sender_name}\n" \
           f"Email: {sender_email}\n" \
           f"Subject: {subject}\n\n" \
           f"Message:\n{message}\n\n" \
           f"Sent on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    encoded_su = urllib.parse.quote(su)
    encoded_body = urllib.parse.quote(body)
    return f"https://mail.google.com/mail/?view=cm&fs=1&to={RECIPIENT_EMAIL}&su={encoded_su}&body={encoded_body}"

def send_contact_email(sender_name, sender_email, subject, message):
    """
    Sends an email notification via SMTP or provides the direct Gmail Compose link.
    Returns (success: bool, status_message: str, gmail_url: str).
    """
    gmail_url = generate_gmail_compose_url(sender_name, sender_email, subject, message)

    if not SENDER_PASSWORD or not SENDER_EMAIL:
        print(f">> [INFO] SMTP credentials not set in .env. Message recorded in database. Direct Gmail Compose URL generated.")
        return False, "Message saved to database! Gmail compose link prepared.", gmail_url

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"📬 Portfolio Message from {sender_name}: {subject or 'General Inquiry'}"
        msg['From'] = f"Mukund Pratap Srivastav Portfolio <{SENDER_EMAIL}>"
        msg['To'] = RECIPIENT_EMAIL
        msg.add_header('Reply-To', sender_email)

        # Plaintext Body
        text_body = f"""New Message from Mukund Pratap Srivastav's Portfolio:

From:    {sender_name} ({sender_email})
Subject: {subject}
Date:    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Message Content:
----------------------------------------
{message}
----------------------------------------
Reply directly to: {sender_email}
"""

        # HTML Body
        html_body = f"""<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #09111a; color: #f2f7f2; padding: 24px; margin: 0;">
  <div style="max-width: 600px; margin: 0 auto; background-color: #0e1824; border: 1px solid #d4af37; border-radius: 12px; padding: 32px; box-shadow: 0 8px 30px rgba(0,0,0,0.6);">
    <div style="border-bottom: 2px solid #c86741; padding-bottom: 16px; margin-bottom: 24px;">
      <h2 style="color: #fdf5c4; margin: 0 0 6px 0; font-size: 22px;">📬 New Contact Submission</h2>
      <p style="color: #c8d8c9; margin: 0; font-size: 14px;">Received on Mukund Pratap Srivastav's Portfolio Website</p>
    </div>
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 24px;">
      <tr>
        <td style="padding: 8px 0; color: #8ba28d; font-weight: 600; width: 100px;">From:</td>
        <td style="padding: 8px 0; color: #f2f7f2; font-weight: bold;">{sender_name}</td>
      </tr>
      <tr>
        <td style="padding: 8px 0; color: #8ba28d; font-weight: 600;">Email:</td>
        <td style="padding: 8px 0; color: #d4af37;"><a href="mailto:{sender_email}" style="color: #d4af37; text-decoration: none;">{sender_email}</a></td>
      </tr>
      <tr>
        <td style="padding: 8px 0; color: #8ba28d; font-weight: 600;">Subject:</td>
        <td style="padding: 8px 0; color: #e2e8f0;">{subject}</td>
      </tr>
    </table>
    <div style="background-color: #09111a; border-left: 4px solid #c86741; padding: 16px 20px; border-radius: 4px; margin-bottom: 28px;">
      <p style="color: #f2f7f2; white-space: pre-wrap; line-height: 1.6; margin: 0; font-size: 15px;">{message}</p>
    </div>
    <div style="text-align: center; border-top: 1px solid #1e3044; padding-top: 20px;">
      <a href="mailto:{sender_email}?subject=Re: {subject}" style="background: linear-gradient(135deg, #7a1733, #c86741); color: #f2f7f2; text-decoration: none; padding: 12px 28px; border-radius: 24px; font-weight: bold; display: inline-block; border: 1px solid #d4af37;">Reply to {sender_name}</a>
    </div>
  </div>
</body>
</html>
"""

        msg.attach(MIMEText(text_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f">> [SUCCESS] Email dispatched to {RECIPIENT_EMAIL} successfully.")
        return True, "Email notification sent to Mukund Pratap Srivastav successfully!", gmail_url

    except Exception as e:
        print(f">> [ERROR] Failed to send email via SMTP: {e}")
        return False, f"SMTP dispatch failed: {e}", gmail_url
