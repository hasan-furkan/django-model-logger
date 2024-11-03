import datetime
import os
import gzip
import shutil
from typing import Optional
from colorama import init, Fore, Style

init(autoreset=True)  # Initialize colorama

class ModelLogger:
    # Define log levels and their priorities
    LOG_LEVELS = {
        'DEBUG': 0,
        'INFO': 1,
        'SUCCESS': 2,
        'WARNING': 3,
        'ERROR': 4
    }

    # ANSI color codes for different log levels
    COLORS = {
        'INFO': Fore.BLUE,
        'SUCCESS': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'DEBUG': Fore.MAGENTA
    }

    def __init__(self, 
                 name: Optional[str] = None, 
                 file_path: Optional[str] = None, 
                 timestamp_format: Optional[str] = "%Y-%m-%d %H:%M:%S",
                 level: str = 'INFO',
                 max_file_size: int = 10 * 1024 * 1024,  # 10MB default
                 backup_count: int = 5,
                 archive_dir: Optional[str] = None):
        self.name = name or "ModelLogger"
        self.file_path = file_path
        self.timestamp_format = timestamp_format
        self.level = level.upper()
        self.max_file_size = max_file_size
        self.backup_count = backup_count
        
        # Set up archive directory
        if file_path and archive_dir is None:
            # Default archive directory is 'logs/archive' in the same directory as the log file
            log_dir = os.path.dirname(os.path.abspath(file_path))
            self.archive_dir = os.path.join(log_dir, 'logs', 'archive')
        else:
            self.archive_dir = archive_dir

        # Create archive directory if it doesn't exist
        if self.file_path and self.archive_dir:
            os.makedirs(self.archive_dir, exist_ok=True)
        
        if self.level not in self.LOG_LEVELS:
            raise ValueError(f"Invalid log level. Choose from {list(self.LOG_LEVELS.keys())}")

    def _get_archive_filename(self) -> str:
        """Generate archive filename with timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.basename(self.file_path)
        return f"{base_name}_{timestamp}.gz"

    def _cleanup_old_archives(self) -> None:
        """Remove old archive files if exceeding backup_count"""
        if not self.archive_dir:
            return

        # Get list of archive files
        archives = []
        for file in os.listdir(self.archive_dir):
            if file.endswith('.gz') and file.startswith(os.path.basename(self.file_path)):
                full_path = os.path.join(self.archive_dir, file)
                archives.append((full_path, os.path.getmtime(full_path)))

        # Sort by modification time (newest first)
        archives.sort(key=lambda x: x[1], reverse=True)

        # Remove excess archives
        for archive_path, _ in archives[self.backup_count:]:
            try:
                os.remove(archive_path)
            except OSError as e:
                print(f"Error removing old archive {archive_path}: {e}")

    def _rotate_log_file(self) -> None:
        """Rotate log files if size exceeds max_file_size"""
        if not self.file_path or not os.path.exists(self.file_path):
            return

        if os.path.getsize(self.file_path) >= self.max_file_size:
            # Generate new archive filename with timestamp
            archive_path = os.path.join(self.archive_dir, self._get_archive_filename())

            # Compress the current log file
            try:
                with open(self.file_path, 'rb') as f_in:
                    with gzip.open(archive_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)

                # Clear the current log file
                open(self.file_path, 'w').close()

                # Cleanup old archives
                self._cleanup_old_archives()

            except Exception as e:
                print(f"Error during log rotation: {e}")

    def _should_log(self, level: str) -> bool:
        """Check if the message should be logged based on current log level"""
        return self.LOG_LEVELS[level] >= self.LOG_LEVELS[self.level]

    def _write_to_file(self, message: str) -> None:
        """Write message to file with rotation check"""
        if not self.file_path:
            return

        # Check and rotate if necessary
        self._rotate_log_file()

        # Write the new log entry
        with open(self.file_path, 'a') as file:
            file.write(message + '\n')

    def _log(self, level: str, message: str) -> None:
        """Log a message with a given level"""
        if not self._should_log(level):
            return

        if self.timestamp_format:
            timestamp = datetime.datetime.now().strftime(self.timestamp_format)
        else:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        color = self.COLORS.get(level, '')
        formatted_message = f"{color}[{timestamp}] {level:<8} {self.name}: {message}{Style.RESET_ALL}"
        plain_message = f"[{timestamp}] {level:<8} {self.name}: {message}"
        
        print(formatted_message)
        if self.file_path:
            self._write_to_file(plain_message)

    def set_level(self, level: str) -> None:
        """Change the log level"""
        level = level.upper()
        if level not in self.LOG_LEVELS:
            raise ValueError(f"Invalid log level. Choose from {list(self.LOG_LEVELS.keys())}")
        self.level = level

    def info(self, message: str) -> None:
        """Log an info message"""
        self._log("INFO", message)

    def success(self, message: str) -> None:
        """Log a success message"""
        self._log("SUCCESS", message)

    def warning(self, message: str) -> None:
        """Log a warning message"""
        self._log("WARNING", message)

    def error(self, message: str) -> None:
        """Log an error message"""
        self._log("ERROR", message)

    def debug(self, message: str) -> None:
        """Log a debug message"""
        self._log("DEBUG", message) 