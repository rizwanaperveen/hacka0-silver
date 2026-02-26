#!/usr/bin/env python3
"""
SMTP Email Sender - Fallback email sending via SMTP
Part of the AI Employee Silver Tier implementation
"""

import os
import sys
import argparse
import smtplib
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration from environment
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')


def send_email_smtp(sender, to, subject, body, cc=None, bcc=None, attachments=None):
    """Send email via SMTP"""

    if not SMTP_USERNAME or not SMTP_PASSWORD:
        print("Error: SMTP credentials not configured.")
        print("Set SMTP_USERNAME and SMTP_PASSWORD in .env file")
        sys.exit(1)

    # Create message
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = to
    message['Subject'] = subject

    if cc:
        message['Cc'] = cc
    if bcc:
        message['Bcc'] = bcc

    # Add body
    message.attach(MIMEText(body, 'plain'))

    # Add attachments
    if attachments:
        for filepath in attachments:
            filepath = Path(filepath)
            if not filepath.exists():
                print(f"Warning: Attachment not found: {filepath}")
                continue

            with open(filepath, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={filepath.name}'
                )
                message.attach(part)

    # Send email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)

            # Collect all recipients
            recipients = [to]
            if cc:
                recipients.extend([r.strip() for r in cc.split(',')])
            if bcc:
                recipients.extend([r.strip() for r in bcc.split(',')])

            server.sendmail(sender, recipients, message.as_string())
            print(f"Email sent successfully via SMTP to {to}")

    except Exception as e:
        print(f"Error sending email via SMTP: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Send email via SMTP')
    parser.add_argument('--from', dest='sender', required=True, help='Sender email address')
    parser.add_argument('--to', required=True, help='Recipient email address')
    parser.add_argument('--subject', required=True, help='Email subject')
    parser.add_argument('--body', required=True, help='Email body')
    parser.add_argument('--cc', help='CC recipients (comma-separated)')
    parser.add_argument('--bcc', help='BCC recipients (comma-separated)')
    parser.add_argument('--attachments', help='Attachment file paths (comma-separated)')

    args = parser.parse_args()

    # Parse attachments
    attachments = None
    if args.attachments:
        attachments = [a.strip() for a in args.attachments.split(',')]

    # Send email
    send_email_smtp(
        args.sender,
        args.to,
        args.subject,
        args.body,
        args.cc,
        args.bcc,
        attachments
    )


if __name__ == "__main__":
    main()
