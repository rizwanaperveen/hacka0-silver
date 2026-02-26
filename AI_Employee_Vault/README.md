# AI Employee - Bronze Tier Implementation

**Personal AI Employee Hackathon 0: Building Autonomous FTEs**

This is a Bronze tier implementation of a Personal AI Employee using Claude Code and Obsidian. The system monitors file drops, processes tasks autonomously, and maintains human-in-the-loop oversight for sensitive actions.

## 🎯 Bronze Tier Requirements

- ✅ Obsidian vault with Dashboard.md and Company_Handbook.md
- ✅ One working Watcher script (file system monitoring)
- ✅ Claude Code reading from and writing to the vault
- ✅ Basic folder structure: /Inbox, /Needs_Action, /Done
- ✅ All AI functionality implemented as Agent Skills

## 📁 Project Structure

```
AI_Employee_Vault/
├── .claude/
│   └── skills/
│       └── process-tasks/          # Claude Code skill for task processing
│           ├── SKILL.md
│           └── prompt.md
├── Inbox/                          # Drop files here for processing
├── Needs_Action/                   # Tasks awaiting AI processing
├── Plans/                          # AI-generated action plans
├── Pending_Approval/               # Actions requiring human approval
├── Approved/                       # Human-approved actions
├── Rejected/                       # Rejected actions
├── Done/                           # Completed tasks
├── Logs/                           # Activity logs
├── Dashboard.md                    # Real-time status overview
├── Company_Handbook.md             # Rules and guidelines
├── base_watcher.py                 # Base class for watchers
├── filesystem_watcher.py           # File system monitoring script
├── pyproject.toml                  # Python project configuration
└── README.md                       # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.13+ installed
- UV package manager installed
- Claude Code installed and configured
- Obsidian (optional, for GUI viewing)

### Installation

1. **Navigate to the vault directory:**
   ```bash
   cd AI_Employee_Vault
   ```

2. **Install Python dependencies:**
   ```bash
   uv sync
   ```

3. **Verify the skill is recognized:**
   ```bash
   claude --list-skills
   ```
   You should see `process-tasks` in the list.

### Running the System

#### Step 1: Start the File Watcher

The watcher monitors the `Inbox/` folder for new files and automatically creates tasks.

```bash
uv run python filesystem_watcher.py
```

Keep this running in a terminal. You should see:
```
Starting Filesystem Watcher
Watching: D:\D drive Data\hacka0-bronze\AI_Employee_Vault\Inbox
Watcher is now active. Press Ctrl+C to stop.
```

#### Step 2: Drop a Test File

In another terminal or file explorer, create a test file in the Inbox:

```bash
echo "This is a test document for processing" > Inbox/test_document.txt
```

The watcher will automatically:
- Detect the new file
- Copy it to `Needs_Action/`
- Create a metadata file describing the task

#### Step 3: Process Tasks with Claude Code

Run the Claude Code skill to process pending tasks:

```bash
claude /process-tasks
```

Claude will:
1. Read the Company_Handbook.md for guidelines
2. Scan Needs_Action/ for pending tasks
3. Analyze each task
4. Create action plans in Plans/
5. Execute safe actions or request approval
6. Update Dashboard.md
7. Move completed tasks to Done/

#### Step 4: Review the Dashboard

Check the updated dashboard:

```bash
cat Dashboard.md
```

Or open it in Obsidian for a better viewing experience.

## 📋 How It Works

### 1. Perception Layer (Watcher)

The `filesystem_watcher.py` script continuously monitors the `Inbox/` folder:

- **Detects** new files dropped into Inbox
- **Creates** task metadata in Needs_Action/
- **Logs** all activity to Logs/

### 2. Reasoning Layer (Claude Code)

When you run `/process-tasks`, Claude Code:

- **Reads** Company_Handbook.md for decision rules
- **Analyzes** tasks in Needs_Action/
- **Determines** priority and required actions
- **Creates** detailed plans in Plans/
- **Executes** auto-approved actions
- **Requests** human approval for sensitive actions

### 3. Action Layer (Human-in-the-Loop)

For sensitive actions:

1. Claude creates an approval request in `Pending_Approval/`
2. You review the request
3. Move to `Approved/` to proceed or `Rejected/` to cancel
4. Run `/process-tasks` again to execute approved actions

## 🔐 Security & Safety

### Auto-Approved Actions
- Reading and analyzing files
- Creating summaries and reports
- Organizing information
- Updating the Dashboard

### Requires Human Approval
- Sending emails or messages
- Making payments
- Deleting files
- Any external communication

All actions are logged in the `Logs/` folder for audit purposes.

## 📊 Dashboard Overview

The Dashboard.md provides real-time status:

- **System Status**: Active/Inactive
- **Pending Tasks**: Count of items in Needs_Action
- **Recent Activity**: Latest processed tasks
- **Alerts**: Any issues requiring attention

## 📖 Company Handbook

The Company_Handbook.md defines:

- **Communication guidelines**: Tone, style, response times
- **Decision-making authority**: What requires approval
- **Priority classification**: Urgent, High, Normal, Low
- **Security protocols**: Credential handling, logging
- **File organization rules**: Naming conventions, folder structure
- **Error handling**: How to handle failures

You can customize this file to match your specific needs and preferences.

## 🧪 Testing the System

### Test 1: Basic File Processing

1. Start the watcher
2. Drop a text file in Inbox/
3. Run `/process-tasks`
4. Check Dashboard.md for updates
5. Verify task moved to Done/

### Test 2: Approval Workflow

1. Modify Company_Handbook.md to require approval for a specific action
2. Drop a file that triggers that action
3. Run `/process-tasks`
4. Check Pending_Approval/ for the request
5. Move to Approved/
6. Run `/process-tasks` again

### Test 3: Multiple Files

1. Drop 3-5 different files in Inbox/
2. Run `/process-tasks`
3. Verify all tasks are processed
4. Check Logs/ for activity records

## 🔧 Customization

### Modify Watcher Behavior

Edit `filesystem_watcher.py` to:
- Change check interval
- Add file type filtering
- Customize metadata format
- Add additional processing logic

### Customize Decision Rules

Edit `Company_Handbook.md` to:
- Define new priority levels
- Add custom approval rules
- Set response time expectations
- Define security protocols

### Extend the Skill

Edit `.claude/skills/process-tasks/prompt.md` to:
- Add new processing steps
- Change output format
- Add integration with external tools
- Implement custom workflows

## 📝 Logs and Audit Trail

All watcher activity is logged to:
```
Logs/FilesystemWatcher_YYYY-MM-DD.log
```

Task processing logs are stored as JSON in:
```
Logs/YYYY-MM-DD.json
```

## 🐛 Troubleshooting

### Watcher Not Detecting Files

- Ensure the watcher is running (`uv run python filesystem_watcher.py`)
- Check file permissions on the Inbox folder
- Verify the file isn't hidden or temporary (starts with . or ~)

### Skill Not Found

- Run `claude --list-skills` to verify installation
- Ensure you're in the correct directory
- Check that `.claude/skills/process-tasks/` exists

### Claude Not Processing Tasks

- Verify files exist in Needs_Action/
- Check Company_Handbook.md is readable
- Review Claude Code logs for errors

## 🎓 Next Steps (Silver Tier)

To upgrade to Silver tier, add:

1. **Multiple Watchers**: Gmail, WhatsApp, LinkedIn monitoring
2. **MCP Servers**: External action capabilities (email sending)
3. **Scheduling**: Automated daily/weekly processing
4. **Advanced Workflows**: Multi-step task automation

## 📚 Resources

- [Hackathon Documentation](../Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026.md)
- [Claude Code Documentation](https://agentfactory.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows)
- [Agent Skills Guide](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Obsidian Documentation](https://help.obsidian.md/)

## 🤝 Contributing

This is a hackathon project. Feel free to:
- Customize for your needs
- Add new features
- Share improvements with the community

## 📄 License

This project is part of the Panaversity AI Employee Hackathon.

---

**Built with:** Claude Code, Python, Watchdog, Obsidian
**Tier:** Bronze (Foundation)
**Status:** ✅ Complete and Functional
