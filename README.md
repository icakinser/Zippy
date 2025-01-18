# Zipper

A modern, feature-rich file compression utility with support for multiple formats, encryption, and folder monitoring. Works on both Windows and macOS.

## Features

### Compression Options
- Multiple compression formats:
  - ZIP (Fast compression)
  - 7Z (Normal compression)
  - LZMA (Maximum compression)
- Batch processing for multiple files
- File encryption support
- Drag and drop interface
- Recent files history

### Advanced Features
- Folder monitoring:
  - Automatically compress new files
  - Configurable file patterns
  - Minimum file size filters
  - Multiple folder support
- Scheduled compression:
  - Schedule compression tasks for later
  - Batch scheduling support
- File extraction:
  - Support for ZIP, 7Z, and LZMA formats
  - Extract to custom location

### User Interface
- Modern, intuitive interface
- Dark mode support
- File preview before compression
- Progress indicators
- Recent files list
- Customizable settings

## Installation

1. Make sure you have Python 3.8 or higher installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Dependencies
- PyQt6: GUI framework
- py7zr: 7-Zip compression
- cryptography: File encryption
- watchdog: Folder monitoring
- lzma: LZMA compression

## Running the Application

```bash
python zipper.py
```

## How to Use

### Basic Compression
1. Launch the application
2. Either:
   - Drag and drop files onto the window
   - Click "Select Files" to choose files
   - Use "Batch Processing" for multiple files
3. Choose compression settings
4. Select save location
5. Wait for compression to complete

### Folder Monitoring
1. Go to Settings → Folder Monitors
2. Click "Add" to set up a new monitored folder
3. Configure:
   - Folder path
   - File patterns (e.g., *.txt, *.pdf)
   - Minimum file size
4. Files added to monitored folders will be automatically compressed

### Encryption
1. Go to Tools → Set Encryption Password
2. Enter and confirm your password
3. Files will be encrypted during compression

### Scheduled Compression
1. Select files to compress
2. Go to Tools → Schedule Compression
3. Set date and time
4. Compression will run at scheduled time

### Batch Processing
1. Go to File → Batch Processing
2. Select source directory
3. Set file filters
4. Choose to process immediately or schedule

### Extract Files
1. Go to File → Extract Archive
2. Select archive file
3. Choose output directory
4. Click Extract

## Settings

### Compression Profiles
- Fast: ZIP format, quick compression
- Normal: 7Z format, balanced compression
- Maximum: LZMA format, highest compression

### Theme Options
- Light mode (default)
- Dark mode

### Other Settings
- Save current settings as default
- Reset to default settings
- Configure folder monitors
- Clear recent files

## Tips
- Use batch processing for large numbers of files
- Set up folder monitoring for automatic compression
- Use encryption for sensitive files
- Schedule large compression tasks for off-hours
- Check recent files list for quick access to compressed files

## Troubleshooting

If you encounter any issues:
1. Check file permissions
2. Ensure enough disk space
3. Verify file is not in use by another application
4. Check encryption password if extracting encrypted files

## Support

For issues and feature requests, please create an issue in the repository.
