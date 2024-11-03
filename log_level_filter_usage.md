# ModelLogger Usage Guide

ModelLogger is a flexible and feature-rich logging solution that provides colored console output and automatic log rotation capabilities.

## Installation

```bash
pip install django-logging-easy
```

## Basic Usage

### Simple Console Logging

```python
from model_logger import ModelLogger

# Create a basic logger
logger = ModelLogger(name="MyApp")

# Log messages with different levels
logger.debug("Debug message")
logger.info("Information message")
logger.success("Success message")
logger.warning("Warning message")
logger.error("Error message")
```

### File Logging with Rotation

```python
# Create a logger with file output
logger = ModelLogger(
    name="MyApp",
    file_path="logs/app.log",
    max_file_size=1024 * 1024,  # 1MB
    backup_count=5
)

# Logs will be written to both console and file
logger.info("This message goes to both console and file")
```

## Advanced Configuration

### Custom Archive Directory

```python
logger = ModelLogger(
    name="MyApp",
    file_path="logs/app.log",
    archive_dir="logs/custom_archives",
    max_file_size=5 * 1024 * 1024,  # 5MB
    backup_count=10
)
```

### Custom Timestamp Format

```python
logger = ModelLogger(
    name="MyApp",
    timestamp_format="%Y-%m-%d %H:%M:%S.%f"
)
```

### Setting Log Level

```python
# Set minimum log level during initialization
logger = ModelLogger(name="MyApp", level="WARNING")

# Or change it dynamically
logger.set_level("DEBUG")
```

## Log Levels

ModelLogger supports five log levels (in order of increasing priority):

1. DEBUG (lowest)
2. INFO
3. SUCCESS
4. WARNING
5. ERROR (highest)

Messages below the set log level will not be displayed or written to file.

## Output Colors

Each log level has a distinct color in the console:
- DEBUG: Magenta
- INFO: Blue
- SUCCESS: Green
- WARNING: Yellow
- ERROR: Red

## Log Rotation Features

The logger automatically manages log files by:
- Creating compressed backups when file size limit is reached
- Maintaining a specified number of backup files
- Adding timestamps to backup files
- Organizing backups in a dedicated archive directory

### Default Directory Structure

```
logs/
├── app.log                          # Current log file
└── archive/
    ├── app.log_20240315_143022.gz  # Most recent backup
    ├── app.log_20240315_142501.gz
    └── app.log_20240315_141955.gz
```

## Complete Configuration Example

```python
from model_logger import ModelLogger

logger = ModelLogger(
    name="MyApplication",                    # Logger name
    file_path="logs/app.log",               # Log file path
    timestamp_format="%Y-%m-%d %H:%M:%S",   # Custom timestamp format
    level="DEBUG",                          # Minimum log level
    max_file_size=10 * 1024 * 1024,        # 10MB max file size
    backup_count=5,                         # Keep 5 backup files
    archive_dir="logs/archives"             # Custom archive directory
)

# Example usage
logger.debug("Debug information")
logger.info("Processing started")
logger.success("Task completed successfully")
logger.warning("Resource usage high")
logger.error("Connection failed")
```

## Best Practices

1. **Log Level Selection**
   - Use DEBUG for detailed debugging information
   - Use INFO for general operational messages
   - Use SUCCESS for successful operations
   - Use WARNING for concerning but non-critical issues
   - Use ERROR for critical issues that need immediate attention

2. **File Management**
   - Set appropriate `max_file_size` based on your application's logging volume
   - Choose `backup_count` based on how long you need to retain logs
   - Use descriptive logger names to identify the source of logs

3. **Archive Organization**
   - Use custom `archive_dir` for better organization in large applications
   - Monitor archive directory size periodically

## Error Handling

The logger handles various errors gracefully:
- Invalid log levels
- File permission issues
- Directory creation failures
- Rotation and compression errors

## Thread Safety

The logger is designed to be thread-safe and can be used in multi-threaded applications.