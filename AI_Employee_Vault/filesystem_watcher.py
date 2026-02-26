"""
Filesystem Watcher - Monitors Inbox folder for new files
Part of the AI Employee Bronze Tier Implementation
"""

from pathlib import Path
from datetime import datetime
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from base_watcher import BaseWatcher


class InboxFileHandler(FileSystemEventHandler):
    """Handles file system events in the Inbox folder"""

    def __init__(self, watcher):
        self.watcher = watcher

    def on_created(self, event):
        """Called when a file is created in the Inbox"""
        if event.is_directory:
            return

        source = Path(event.src_path)

        # Ignore temporary files and hidden files
        if source.name.startswith('.') or source.name.startswith('~'):
            return

        self.watcher.logger.info(f'New file detected: {source.name}')
        self.watcher.process_file(source)


class FilesystemWatcher(BaseWatcher):
    """Watches the Inbox folder for new files and creates action items"""

    def __init__(self, vault_path: str):
        super().__init__(vault_path, check_interval=5)
        self.inbox = self.vault_path / 'Inbox'
        self.inbox.mkdir(exist_ok=True)
        self.observer = None

    def process_file(self, source: Path):
        """Process a new file dropped in Inbox"""
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            dest_name = f'FILE_{timestamp}_{source.name}'
            dest = self.needs_action / dest_name

            # Copy file to Needs_Action
            shutil.copy2(source, dest)
            self.logger.info(f'Copied file to: {dest.name}')

            # Create metadata file
            self.create_action_file(source)

            # Optionally remove from Inbox (or move to archive)
            # source.unlink()  # Uncomment to delete from Inbox after processing

        except Exception as e:
            self.logger.error(f'Error processing file {source.name}: {e}')

    def check_for_updates(self) -> list:
        """Check Inbox for existing files (initial scan)"""
        files = []
        for file_path in self.inbox.iterdir():
            if file_path.is_file() and not file_path.name.startswith('.'):
                files.append(file_path)
        return files

    def create_action_file(self, source: Path) -> Path:
        """Create metadata file for the dropped file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        meta_path = self.needs_action / f'FILE_{timestamp}_{source.stem}.md'

        # Get file stats
        stats = source.stat()
        file_size = stats.st_size
        file_size_str = self._format_file_size(file_size)

        content = f"""---
type: file_drop
original_name: {source.name}
size: {file_size_str}
size_bytes: {file_size}
received: {datetime.now().isoformat()}
priority: normal
status: pending
---

## New File Dropped for Processing

**File:** {source.name}
**Size:** {file_size_str}
**Location:** Inbox

## Suggested Actions
- [ ] Review file contents
- [ ] Categorize and file appropriately
- [ ] Extract any actionable items
- [ ] Archive or delete after processing

## Notes
Add any relevant notes or observations here.
"""

        meta_path.write_text(content, encoding='utf-8')
        self.logger.info(f'Created metadata file: {meta_path.name}')
        return meta_path

    def _format_file_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"

    def run(self):
        """Start watching the Inbox folder"""
        self.logger.info(f'Starting Filesystem Watcher')
        self.logger.info(f'Watching: {self.inbox}')

        # Process any existing files first
        existing_files = self.check_for_updates()
        if existing_files:
            self.logger.info(f'Processing {len(existing_files)} existing file(s)')
            for file_path in existing_files:
                self.process_file(file_path)

        # Start watching for new files
        event_handler = InboxFileHandler(self)
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.inbox), recursive=False)
        self.observer.start()

        self.logger.info('Watcher is now active. Press Ctrl+C to stop.')

        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info('Stopping watcher...')
            self.observer.stop()
            self.observer.join()
            self.logger.info('Watcher stopped')


if __name__ == '__main__':
    # Get vault path (assumes script is in vault directory)
    vault_path = Path(__file__).parent

    # Create and run watcher
    watcher = FilesystemWatcher(str(vault_path))
    watcher.run()
