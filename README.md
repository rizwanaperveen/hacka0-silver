# AI Employee - Silver Tier

Your autonomous AI Employee built with Claude Code, Obsidian, and Python watchers.

## What is This?

This is a **Silver Tier** implementation of the Personal AI Employee from the Panaversity Hackathon 0. It's an autonomous system that:

- 📧 Monitors Gmail for important emails
- 💬 Watches WhatsApp for urgent messages
- 💼 Tracks LinkedIn for engagement opportunities
- 🤖 Uses Claude Code to reason and plan actions
- ✅ Implements human-in-the-loop approval for sensitive actions
- 📊 Maintains a dashboard in Obsidian

## Features

### Watchers (Perception Layer)
- **Gmail Watcher**: Monitors important unread emails
- **WhatsApp Watcher**: Detects urgent messages with keywords
- **LinkedIn Watcher**: Tracks messages and posting opportunities

### Skills (Action Layer)
- `/process-tasks`: Process items from Needs_Action folder
- `/create-plan`: Generate detailed action plans
- `/send-email`: Draft and send emails with approval
- `/linkedin-post`: Create and post LinkedIn content
- `/approve-actions`: Execute approved actions

### Approval Workflow
- Sensitive actions require human approval
- Draft → Pending_Approval → Human Review → Approved → Execute
- 24-hour expiration on approval requests

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Claude Code CLI
- Obsidian (optional, for GUI)

### Installation

```bash
# Clone or download this repository
cd hacka0-silver

# Run setup script (Mac/Linux)
bash setup.sh

# Or manually:
pip install -r watchers/requirements.txt
playwright install chromium
npm install -g pm2
```

### Configuration

1. **Set up Gmail API**:
   - Follow guide in `watchers/README.md`
   - Download credentials to `watchers/credentials/gmail_credentials.json`

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Customize vault files**:
   - Edit `AI_Employee_Vault/Company_Handbook.md`
   - Edit `AI_Employee_Vault/Business_Goals.md`

### Start Watchers

```bash
# Start all watchers with PM2
pm2 start watchers/gmail_watcher.py --interpreter python3 --name gmail
pm2 start watchers/whatsapp_watcher.py --interpreter python3 --name whatsapp
pm2 start watchers/linkedin_watcher.py --interpreter python3 --name linkedin

# Save configuration
pm2 save
pm2 startup
```

### Test Skills

```bash
cd AI_Employee_Vault

# Process tasks
claude /process-tasks

# Create a plan
claude /create-plan "task: prepare monthly report"

# Draft LinkedIn post
claude /linkedin-post

# Process approvals
claude /approve-actions
```

## Project Structure

```
hacka0-silver/
├── AI_Employee_Vault/          # Obsidian vault
│   ├── Dashboard.md            # Main dashboard
│   ├── Company_Handbook.md     # Guidelines and rules
│   ├── Business_Goals.md       # Business objectives
│   ├── Needs_Action/           # Tasks to process
│   ├── Plans/                  # Action plans
│   ├── Pending_Approval/       # Awaiting approval
│   ├── Approved/               # Approved actions
│   ├── Done/                   # Completed tasks
│   └── Logs/                   # Activity logs
├── watchers/                   # Perception layer
│   ├── gmail_watcher.py
│   ├── whatsapp_watcher.py
│   ├── linkedin_watcher.py
│   └── requirements.txt
├── scripts/                    # Helper scripts
│   ├── gmail_api.py
│   └── send_smtp.py
└── .claude/skills/             # Claude Code skills
    ├── process-tasks/
    ├── create-plan/
    ├── send-email/
    ├── linkedin-post/
    └── approve-actions/
```

## How It Works

### 1. Perception (Watchers)
Lightweight Python scripts monitor external services:
- Gmail API for important emails
- WhatsApp Web via Playwright
- LinkedIn via Playwright

When they detect something important, they create task files in `/Needs_Action/`.

### 2. Reasoning (Claude Code)
Claude Code processes tasks using skills:
- Reads context from vault files
- Creates detailed plans
- Drafts responses
- Requests approval for sensitive actions

### 3. Action (MCP Servers)
After approval, Claude executes actions:
- Sends emails via Gmail API
- Posts on LinkedIn via Playwright
- Updates dashboard
- Logs all activities

### 4. Human-in-the-Loop
You maintain control:
- Review drafts in `/Pending_Approval/`
- Edit if needed
- Move to `/Approved/` to execute
- Move to `/Rejected/` to cancel

## Silver Tier Checklist

- [x] Gmail watcher implemented
- [x] WhatsApp watcher implemented
- [x] LinkedIn watcher implemented
- [x] Task processing skill
- [x] Plan creation skill
- [x] Email sending skill
- [x] LinkedIn posting skill
- [x] Approval workflow skill
- [x] Human-in-the-loop approval
- [x] All functionality as Agent Skills
- [ ] Scheduling configured (cron/Task Scheduler)
- [ ] End-to-end testing complete
- [ ] Demo video recorded

## Documentation

- **[SILVER_TIER_SETUP.md](SILVER_TIER_SETUP.md)**: Complete setup guide
- **[watchers/README.md](watchers/README.md)**: Watcher configuration
- **[Personal AI Employee Hackathon 0.md](Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026.md)**: Full hackathon documentation

## Troubleshooting

### Watchers not creating tasks
- Check logs: `pm2 logs [watcher-name]`
- Verify credentials configured
- Ensure vault path is correct

### Skills not working
- Verify in vault directory: `cd AI_Employee_Vault`
- Check skill files exist: `ls .claude/skills/`
- Run `claude --help` to see available skills

### Approvals not executing
- Verify files in `/Approved/` folder
- Check file format (YAML frontmatter)
- Ensure not expired (24 hours)

## Security

- Never commit `.env` file
- Keep credentials in `credentials/` folder (gitignored)
- Review approval requests before approving
- Check logs regularly for unexpected activity
- Use app-specific passwords for Gmail

## Next Steps

After completing Silver Tier:
- **Gold Tier**: Add more integrations (Facebook, Twitter, Odoo)
- **Platinum Tier**: Deploy to cloud for 24/7 operation
- **Advanced**: Implement Ralph Wiggum loop for full autonomy

## Support

- **Weekly Research Meeting**: Wednesdays 10 PM
- **Zoom**: https://us06web.zoom.us/j/87188707642
- **Submit Form**: https://forms.gle/JR9T1SJq5rmQyGkGA
- **YouTube**: https://www.youtube.com/@panaversity

## License

This is a hackathon project for educational purposes.

## Acknowledgments

Built for Panaversity's Personal AI Employee Hackathon 0.
Powered by Claude Code, Anthropic's official CLI.

---

**Status**: Silver Tier 🥈
**Last Updated**: 2026-02-26
