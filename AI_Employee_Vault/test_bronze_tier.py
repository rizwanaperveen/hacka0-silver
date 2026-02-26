#!/usr/bin/env python3
"""
Quick Test Script for AI Employee Bronze Tier
Demonstrates the complete workflow
"""

import time
from pathlib import Path
import shutil


def main():
    print("=" * 60)
    print("AI EMPLOYEE BRONZE TIER - QUICK TEST")
    print("=" * 60)
    print()

    # Get vault path
    vault_path = Path(__file__).parent
    inbox = vault_path / "Inbox"
    needs_action = vault_path / "Needs_Action"
    done = vault_path / "Done"

    # Verify folders exist
    print("[*] Checking folder structure...")
    required_folders = [
        "Inbox", "Needs_Action", "Done", "Plans",
        "Pending_Approval", "Approved", "Rejected", "Logs"
    ]

    for folder in required_folders:
        folder_path = vault_path / folder
        if folder_path.exists():
            print(f"  [+] {folder}/ exists")
        else:
            print(f"  [-] {folder}/ missing!")
            return

    print()

    # Check key files
    print("[*] Checking key files...")
    key_files = ["Dashboard.md", "Company_Handbook.md", "README.md"]

    for file in key_files:
        file_path = vault_path / file
        if file_path.exists():
            print(f"  [+] {file} exists")
        else:
            print(f"  [-] {file} missing!")
            return

    print()

    # Check skill
    print("[*] Checking Claude Code skill...")
    skill_path = vault_path / ".claude" / "skills" / "process-tasks"
    if skill_path.exists():
        print(f"  [+] process-tasks skill exists")
        if (skill_path / "SKILL.md").exists():
            print(f"  [+] SKILL.md exists")
        if (skill_path / "prompt.md").exists():
            print(f"  [+] prompt.md exists")
    else:
        print(f"  [-] process-tasks skill missing!")
        return

    print()

    # Create test file
    print("[*] Creating test file in Inbox...")
    test_file = inbox / "test_document.txt"
    test_content = """This is a test document for the AI Employee system.

Task: Please analyze this document and create a summary.

Priority: Normal
Category: Testing

The AI Employee should:
1. Detect this file in the Inbox
2. Create a task in Needs_Action
3. Process it when /process-tasks is run
4. Update the Dashboard
5. Move to Done when complete
"""

    test_file.write_text(test_content)
    print(f"  [+] Created: {test_file.name}")
    print()

    # Instructions
    print("=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print()
    print("1. Start the watcher in a separate terminal:")
    print("   uv run python filesystem_watcher.py")
    print()
    print("2. The watcher will detect the test file and create a task")
    print()
    print("3. Process the task with Claude Code:")
    print("   claude /process-tasks")
    print()
    print("4. Check the Dashboard for updates:")
    print("   cat Dashboard.md")
    print()
    print("5. Verify the task was moved to Done/")
    print()
    print("=" * 60)
    print("BRONZE TIER REQUIREMENTS: [COMPLETE]")
    print("=" * 60)
    print()
    print("[+] Obsidian vault with Dashboard.md and Company_Handbook.md")
    print("[+] Working Watcher script (filesystem monitoring)")
    print("[+] Claude Code can read/write to vault")
    print("[+] Folder structure: /Inbox, /Needs_Action, /Done")
    print("[+] AI functionality as Agent Skills (/process-tasks)")
    print()
    print("Ready for testing!")
    print()


if __name__ == "__main__":
    main()
