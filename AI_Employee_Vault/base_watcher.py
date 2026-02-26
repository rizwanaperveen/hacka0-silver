"""
Base Watcher Class - Template for all watchers
Part of the AI Employee Bronze Tier Implementation
"""

import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime


class BaseWatcher(ABC):
    """Abstract base class for all watcher implementations"""

    def __init__(self, vault_path: str, check_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """Configure logging for this watcher"""
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # File handler
        log_dir = self.vault_path / 'Logs'
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / f'{self.__class__.__name__}_{datetime.now().strftime("%Y-%m-%d")}.log'
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger

    @abstractmethod
    def check_for_updates(self) -> list:
        """
        Check for new items to process
        Returns: list of new items
        """
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        """
        Create .md file in Needs_Action folder
        Returns: Path to created file
        """
        pass

    def run(self):
        """Main loop - continuously check for updates"""
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Monitoring vault at: {self.vault_path}')
        self.logger.info(f'Check interval: {self.check_interval} seconds')

        while True:
            try:
                items = self.check_for_updates()
                if items:
                    self.logger.info(f'Found {len(items)} new item(s) to process')
                    for item in items:
                        file_path = self.create_action_file(item)
                        self.logger.info(f'Created action file: {file_path.name}')
                else:
                    self.logger.debug('No new items found')

            except KeyboardInterrupt:
                self.logger.info('Watcher stopped by user')
                break
            except Exception as e:
                self.logger.error(f'Error in watcher loop: {e}', exc_info=True)

            time.sleep(self.check_interval)
