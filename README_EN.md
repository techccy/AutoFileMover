# AutoFileMover

[「中文」](README.md)

An automatic file transfer program designed specifically for Windows that monitors a specified directory and automatically classifies and moves files to designated folders based on rules after ensuring file download or transfer completion and file integrity.

## Features

- 🎯 **Smart Monitoring**: Real-time monitoring of file changes in specified directories
- ✅ **Integrity Check**: Ensures files are completely downloaded before processing
- 📁 **Smart Classification**: Automatically categorizes and moves files to corresponding directories based on file types
- 🖥️ **System Tray**: Resident system tray with right-click menu operations
- ⚙️ **Flexible Configuration**: Customizable rules through YAML configuration files
- 🔔 **Instant Notifications**: Desktop notifications with "Open File" button after file processing
- 🪟 **Windows Optimized**: Specifically optimized for Windows platform

## Installation

1. Clone the project:
```bash
git clone https://github.com/yourusername/AutoFileMover.git
cd AutoFileMover
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or using pipenv:
```bash
pipenv install
```

## Configuration

The program uses a `config.yaml` file for configuration:

```yaml
# Directory path to monitor
watch_directory: "~/Downloads"

# Enable debug mode
debug: false

# Log file path
log_file: "autofilemover.log"

# File integrity check delay (seconds)
integrity_check_delay: 2

# Target directories after moving
target_directories:
  documents: "~/Documents/Organized/Documents"
  images: "~/Documents/Organized/Images"
  videos: "~/Documents/Organized/Videos"
  music: "~/Documents/Organized/Music"
  archives: "~/Documents/Organized/Archives"
  others: "~/Documents/Organized/Others"

# File classification rules
rules:
  - name: "Document Files"
    extensions: [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"]
    target: "documents"
    
  - name: "Image Files"
    extensions: [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"]
    target: "images"
    
  - name: "Video Files"
    extensions: [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"]
    target: "videos"
    
  - name: "Audio Files"
    extensions: [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"]
    target: "music"
    
  - name: "Archive Files"
    extensions: [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"]
    target: "archives"
    
  - name: "Executable Files"
    extensions: [".exe", ".msi", ".bat", ".cmd"]
    target: "others"
    notify: true  # Send special notification for these files

# Default target directory (for files not matching any rules)
default_target: "others"

# Notification settings
notifications:
  enabled: true
  sound: true
```

## Usage

1. Modify the `config.yaml` configuration file to suit your needs
2. Run the program:
```bash
python start.py
```

Or double-click the `start.bat` file on Windows.

3. The program will run in the system tray. Right-click the icon to:
   - **Open Config**: Open the configuration file for editing
   - **Reload Config**: Reload the configuration file (without restarting the program)
   - **Stop Work**: Exit the program

## System Tray Menu

- **Open Config**: Quickly open the YAML configuration file for editing
- **Reload Config**: Reload the configuration file to make changes take effect immediately
- **Stop Work**: Safely exit the program

## Notification Feature

The program sends desktop notifications after file processing is complete. The notification window includes:
- File processing result information
- "Open File" button to directly access the processed file
- "OK" button to close the notification
- Automatically closes after 8 seconds

## Development

### Project Structure

```
AutoFileMover/
├── start.py                  # Program startup script
├── start.bat                 # Windows batch startup file
├── main.py                   # Main program entry
├── config_manager.py         # Configuration manager
├── file_watcher.py           # File watcher
├── file_integrity_checker.py # File integrity checker
├── rule_engine.py            # Rule engine
├── file_mover.py             # File mover
├── notification_manager.py   # Notification manager
├── tray_manager.py           # System tray manager
├── config.yaml               # Configuration file
├── requirements.txt          # Dependency list
├── test_functionality.py     # Functionality test script
├── build_windows_exe.bat     # Windows packaging script
├── README.md                 # Documentation
└── LICENSE                   # License file
```

### Adding New File Classification Rules

Add new rules in the `rules` section of `config.yaml`:

```yaml
  - name: "New File Type"
    extensions: [".ext1", ".ext2"]
    target: "target_category"
    notify: true  # Optional, send notification for these files
```

## Packaging as Windows Executable

To package the program as a Windows executable (.exe), follow these steps:

### Method 1: Using PyInstaller Command Line (Recommended)

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Run the packaging command:
```bash
pyinstaller --onefile --windowed ^
    --name AutoFileMover ^
    --add-data "config.yaml;." ^
    --add-data "icons;icons" ^
    --add-data "README.md;." ^
    --hidden-import tkinter ^
    --hidden-import tkinter.messagebox ^
    --hidden-import PIL ^
    --hidden-import yaml ^
    --hidden-import watchdog ^
    --hidden-import pystray ^
    start.py
```

3. After packaging is complete, you can find `AutoFileMover.exe` in the `dist` directory.

### Method 2: Using Batch Script

Directly run the `build_windows_exe.bat` script in the project, which will automatically complete the above steps.

## Deployment to Other Windows Computers

Copy the following files to the target computer to run:

1. `dist/AutoFileMover.exe` - Main program
2. `config.yaml` - Configuration file (can be modified as needed)
3. `start.bat` - Startup script (optional)

Note: The target computer needs to have Python environment to run certain functions. It is recommended to install a complete Python distribution.

## Contributing

Contributions of any form are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for information on how to participate in project development.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
