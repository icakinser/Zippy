# Zipper User Guide

Welcome to Zipper! This guide will help you get started with compressing and managing your files.

## Quick Start Guide

### Basic File Compression
1. **Start the app** - Launch Zipper from your applications menu
2. **Add files** - You can:
   - Drag and drop files onto the main window
   - Click "Select Files" to browse for files
   - Drop multiple files at once
3. **Choose settings** - Select your compression preferences:
   - Fast (ZIP) - Best for quick compression
   - Normal (7Z) - Good balance of size and speed
   - Maximum (LZMA) - Best compression, but slower
4. **Save** - Choose where to save your compressed file

That's it! Your files are now compressed.

## Features Guide

### Working with Files

#### Compressing Files
- **Single File**
  1. Drop the file onto the window
  2. Select compression level
  3. Choose save location
  
- **Multiple Files**
  1. Select multiple files in your file browser
  2. Drag them all at once
  3. They'll be combined into one archive

#### Extracting Files
1. Click File → Extract Archive
2. Select your compressed file
3. Choose where to extract
4. Click Extract

### Batch Processing
Process many files at once:
1. Click File → Batch Processing
2. Select a folder containing your files
3. Set file filters (e.g., *.jpg, *.pdf)
4. Choose to:
   - Process now
   - Schedule for later

### Folder Monitoring
Let Zipper automatically compress new files:

1. **Set Up**
   - Go to Settings → Folder Monitors
   - Click "Add"
   - Choose a folder to monitor
   
2. **Configure**
   - Set file patterns (*.txt, *.pdf, etc.)
   - Set minimum file size
   - Choose compression settings

3. **Use**
   - Drop files into monitored folders
   - They'll be compressed automatically
   - Find compressed files in a 'compressed' subfolder

### Scheduling
Schedule compression tasks:

1. Select your files
2. Go to Tools → Schedule Compression
3. Set date and time
4. Files will be compressed automatically at the scheduled time

### File Security

#### Encrypting Files
1. Go to Tools → Set Encryption Password
2. Enter a strong password
3. Your next compression will be encrypted
4. Keep your password safe - you'll need it to extract files!

## Tips & Tricks

### Compression Profiles
- **Fast (ZIP)**
  - Best for: Quick compression, sharing files
  - File type: .zip
  - Good compatibility with other programs

- **Normal (7Z)**
  - Best for: Everyday use
  - File type: .7z
  - Better compression than ZIP

- **Maximum (LZMA)**
  - Best for: Long-term storage
  - File type: .xz
  - Smallest file size

### Keyboard Shortcuts
- **Ctrl/Cmd + O**: Open files
- **Ctrl/Cmd + B**: Batch processing
- **Ctrl/Cmd + E**: Extract archive
- **Ctrl/Cmd + H**: Show this help

### Best Practices
1. **Organizing Files**
   - Keep similar files together
   - Use meaningful archive names
   - Use batch processing for large groups

2. **Monitoring Folders**
   - Monitor download folders for automatic compression
   - Set appropriate file patterns
   - Check compressed folder regularly

3. **File Security**
   - Use encryption for sensitive files
   - Keep passwords in a safe place
   - Test encrypted archives after creating them

## Customization

### Theme Settings
1. Go to Settings → Theme
2. Choose:
   - Light Mode (default)
   - Dark Mode

### Default Settings
- Save your preferred settings:
  1. Configure the app as you like
  2. Go to Settings → Save Current Settings
  
- Reset to defaults:
  1. Go to Settings → Reset to Default Settings

## Troubleshooting

### Common Issues

**Files won't compress?**
- Check if files are in use
- Ensure enough disk space
- Try a different compression level

**Can't extract files?**
- Verify the archive isn't corrupted
- Check if you have write permission
- For encrypted files, verify password

**Folder monitoring not working?**
- Check folder permissions
- Verify file patterns are correct
- Ensure enough disk space

### Need More Help?
- Check our online documentation
- Contact support
- Report issues on our repository

## Quick Reference

### File Formats
- **.zip** - Most compatible
- **.7z** - Better compression
- **.xz** - Best compression

### Size Guidelines
- Small files (<10MB): Fast compression
- Medium files (10-100MB): Normal compression
- Large files (>100MB): Maximum compression

### Memory Usage
- Keep enough free space
- At least twice the size of files being compressed
- More for maximum compression
