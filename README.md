# 📽️ Chapter Maker

A modern GUI application that parses CSV files to extract and format chapter timestamps. The application provides an easy way to copy or save formatted chapter timestamps for video editing or content creation.

## ✨ Features

- 🌙 Modern dark mode interface
- 📄 CSV file parsing with automatic formatting
- ⏱️ Time format conversion (extracts minutes:seconds from timecode)
- 📋 One-click copy of all chapters
- 💾 Save chapters to text file
- 🖥️ Cross-platform support (macOS, Windows, Linux)
- 📁 Source directory-based file saving

## 📋 Requirements

- Python 3.x
- Virtual environment (recommended)
- Dependencies listed in `requirements.txt`

## 🚀 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd chapter-maker
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:

On macOS/Linux:
```bash
source venv/bin/activate
```

On Windows:
```bash
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📖 Usage

1. Run the application:
```bash
python modern_chapter_maker.py
```

2. Use the interface:
   - Click "Select CSV File" to choose your CSV file
   - The parsed chapters will appear in the table
   - Click "Copy All Chapters" to copy all chapters to clipboard
   - Click "Save Chapters" to save the chapters to a text file

## 📊 CSV Format

The application expects a CSV file with the following columns:
- `Record In`: Timestamp in format HH:MM:SS:FF
- `Notes`: Chapter title/description

The application will:
- Extract only the minutes and seconds from the timestamp
- Combine the time with the notes
- Format each line as: `MM:SS Chapter Title`

## 📤 Output Format

The copied or saved chapters will be formatted as:
```
MM:SS Chapter Title
MM:SS Next Chapter
...
