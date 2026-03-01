# Gmail API Credentials Setup Guide

## Quick Setup (5-10 minutes)

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it: "AI-Employee-Gmail"
4. Click "Create"

### Step 2: Enable Gmail API

1. In the search bar, type "Gmail API"
2. Click on "Gmail API"
3. Click "Enable"

### Step 3: Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: **External**
   - App name: "AI Employee"
   - User support email: Your email
   - Developer contact: Your email
   - Click "Save and Continue"
   - Scopes: Skip for now
   - Test users: Add your Gmail address
   - Click "Save and Continue"

4. Back to Create OAuth client ID:
   - Application type: **Desktop app**
   - Name: "AI Employee Desktop"
   - Click "Create"

5. Download the JSON file:
   - Click "Download JSON" button
   - Save as `gmail_credentials.json` in this folder

### Step 4: Verify File Location

The file should be at:
```
D:\D drive Data\hacka0-silver\watchers\credentials\gmail_credentials.json
```

### Step 5: First Run (Authentication)

```bash
cd D:\D drive Data\hacka0-silver\watchers
python gmail_watcher.py
```

- A browser window will open
- Sign in with your Gmail account
- Click "Allow" to grant permissions
- The token will be saved for future use

## File Structure

After setup, you should have:
```
credentials/
├── README.md (this file)
├── gmail_credentials.json (OAuth client credentials)
└── gmail_token.json (auto-generated after first auth)
```

## Troubleshooting

### Error: "Credentials file not found"
- Make sure `gmail_credentials.json` is in the `credentials/` folder
- Check the filename is exactly `gmail_credentials.json` (not .txt)

### Error: "Access blocked: This app's request is invalid"
- Add your email to "Test users" in OAuth consent screen
- Make sure app is in "Testing" mode (not "Production")

### Error: "invalid_grant"
- Delete `gmail_token.json`
- Run the watcher again to re-authenticate

### Browser doesn't open
- Check if port 8080 is available
- Try running as administrator

## Security Notes

- ✅ These files are in `.gitignore` (won't be committed)
- ✅ Keep credentials private
- ✅ Don't share `gmail_credentials.json` or `gmail_token.json`
- ✅ Rotate credentials if compromised

## Alternative: Use SMTP Instead

If you don't want to set up Gmail API, you can use SMTP for sending emails:

1. Enable 2-factor authentication on your Gmail
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the app password in `.env` file:
   ```
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   ```

Note: SMTP only works for sending emails, not reading them. For reading emails, you need Gmail API.

## Quick Test

After setup, test the credentials:

```bash
python test_gmail_credentials.py
```

This will verify your credentials work without starting the full watcher.
