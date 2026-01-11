# ChronoPhantom

```
    ▄████▄   ██░ ██  ██▀███   ▒█████   ███▄    █  ▒█████  
   ▒██▀ ▀█  ▓██░ ██▒▓██ ▒ ██▒▒██▒  ██▒ ██ ▀█   █ ▒██▒  ██▒
   ▒▓█    ▄ ▒██▀▀██░▓██ ░▄█ ▒▒██░  ██▒▓██  ▀█ ██▒▒██░  ██▒
   ▒▓▓▄ ▄██▒░▓█ ░██ ▒██▀▀█▄  ▒██   ██░▓██▒  ▐▌██▒▒██   ██░
   ▒ ▓███▀ ░░▓█▒░██▓░██▓ ▒██▒░ ████▓▒░▒██░   ▓██░░ ████▓▒░
   PHANTOM
```

> Professional timestamp manipulation and metadata removal suite for Windows

[![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## Overview

**ChronoPhantom** is a powerful Windows CLI tool designed for precision control over file timestamps and metadata. Built for security researchers, forensic analysts, and power users who need complete control over temporal file attributes.

### Core Capabilities

**Timestamp Manipulation**
- Rewrite NTFS creation timestamps
- Modify last access times
- Control modification dates
- Batch processing for directories

**Metadata Removal**
- Strip EXIF data from images (JPG, PNG, TIFF, HEIC)
- Remove metadata from videos (MP4, MKV, AVI, MOV)
- Clean audio file metadata (MP3, WAV, FLAC)
- FFmpeg-powered container rewrites

**Interface**
- Modern cyberpunk-themed CLI
- Color-coded operations
- Real-time progress feedback
- Intuitive menu system

---

## Quick Start

### Prerequisites

```
Windows OS (NTFS filesystem)
Python 3.7 or higher
ExifTool
FFmpeg
```

### Installation

**Clone the repository**
```bash
git clone https://github.com/yourusername/chronophantom.git
cd chronophantom
```

**Install dependencies**
```bash
pip install -r requirements.txt
```

**Setup external tools**

Download and add to PATH:
- [ExifTool](https://exiftool.org/) - Image metadata manipulation
- [FFmpeg](https://ffmpeg.org/download.html) - Media file processing

### Run

```bash
python chronophantom.py
```

---

## Usage

### Main Menu

```
[1] Single File Timestamp        - Modify one file
[2] Batch Directory Processing   - Recursive operation
[3] Deep Clean (Metadata Wipe)   - Maximum stealth
[4] Information                  - About this tool
[5] Exit                         - Close application
```

### Date Format

```
YYYY-MM-DD
2024-01-15

YYYY-MM-DD HH:MM:SS
2024-01-15 14:30:00
```

### Example Workflow

```
Select option: 3
Target path: C:\Documents\vacation_photos
Target date: 2020-06-15 10:30:00

Processing...
✓ Cleaning metadata...
✓ SUCCESS | C:\Documents\vacation_photos\IMG_001.jpg
✓ SUCCESS | C:\Documents\vacation_photos\IMG_002.jpg
✓ Processed 47 files

OPERATION COMPLETE
```

---

## Features Deep Dive

### Timestamp Precision

ChronoPhantom directly manipulates Windows NTFS timestamps at the kernel level using the Win32 API. This ensures:
- Accurate timestamp modification down to the second
- Proper FILETIME structure handling
- No filesystem caching issues
- Persistent changes across reboots

### Metadata Removal

**Images**
- Complete EXIF data strip
- GPS coordinates removal
- Camera information deletion
- Software metadata cleaning

**Media Files**
- Container-level metadata removal
- Embedded thumbnail deletion
- Track information cleaning
- Codec metadata preservation (for playback compatibility)

---

## Technical Details

### Architecture

```
ChronoPhantom
├── Windows API Integration (ctypes)
├── ExifTool Wrapper
├── FFmpeg Processor
└── CLI Interface (colorama)
```

### Supported File Types

| Category | Extensions |
|----------|-----------|
| Images   | .jpg, .jpeg, .png, .tiff, .heic |
| Videos   | .mp4, .mkv, .avi, .mov |
| Audio    | .mp3, .wav, .flac |

---

## Security Notice

This tool is designed for legitimate use cases including:
- Digital forensics research and training
- File management and organization
- Privacy protection for personal files
- Testing and development environments

Users are solely responsible for ensuring proper authorization before modifying file attributes or metadata. ChronoPhantom developers assume no liability for misuse.

---

## Contributing

Contributions are welcome. Please ensure:
- Code follows existing style conventions
- Features are tested on Windows 10/11
- Documentation is updated accordingly

---

## License

MIT License - see [LICENSE](LICENSE) for details

---

## Credits

**Developer**: [Slay]  
**Philosophy**: "If time is evidence, we erase the clock."

Built with Python, powered by ExifTool and FFmpeg.
