#!/usr/bin/env python3
"""
Gmail API Helper - Send emails via Gmail API
Part of the AI Employee Silver Tier implementation
"""

import os
import sys
import argparse
import base64
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    import pickle
except ImportError:
    print("Error: Gmail API libraries not installed.")
    print("Install with: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

# Configuration
CREDENTIALS_PATH = Path(__file__).parent / "credentials" / "gmail_credentials.json"
TOKEN_PATH = Path(__file__).parent / "credentials" / "gmail_token.pickle"
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def authenticate():
    """Authenticate with Gmail API"""
    creds = None

    # Load existing token
    if TOKEN_PATH.exists():
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_PATH.exists():
                print(f"Error: Credentials file not found: {CREDENTIALS_PATH}")
                print("Download credentials from Google Cloud Console")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials
        TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)


def create_message(sender, to, subject, body, cc=None, bcc=None, attachments=None):
    """Create email message"""
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    if cc:
        message['cc'] = cc
    if bcc:
        message['bcc'] = bcc

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

    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def send_email(service, sender, to, subject, body, cc=None, bcc=None, attachments=None):
    """Send email via Gmail API"""
    try:
        message = create_message(sender, to, subject, body, cc, bcc, attachments)
        result = service.users().messages().send(userId='me', body=message).execute()
        print(f"Email sent successfully. Message ID: {result['id']}")
        return result
    except Exception as e:
        print(f"Error sending email: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Send email via Gmail API')
    parser.add_argument('--from', dest='sender', required=True, help='Sender email address')
    parser.add_argument('--to', required=True, help='Recipient email address')
    parser.add_argument('--subject', required=True, help='Email subject')
    parser.add_argument('--body', required=True, help='Email body')
    parser.add_argument('--cc', help='CC recipients (comma-separated)')
    parser.add_argument('--bcc', help='BCC recipients (comma-separated)')
    parser.add_argument('--attachments', help='Attachment file paths (comma-separated)')

    args = parser.parse_args()

    # Authenticate
    service = authenticate()

    # Parse attachments
    attachments = None
    if args.attachments:
        attachments = [a.strip() for a in args.attachments.split(',')]

    # Send email
    send_email(
        service,
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
