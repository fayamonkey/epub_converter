# EPUB Converter

A simple web-based tool to convert EPUB files to text or markdown format. This tool extracts content from EPUB files without editing it, preserving the original structure and formatting.

## Features

- 📚 **EPUB Support**: Convert any standard EPUB file
- 📄 **Multiple Formats**: Output as plain text (.txt) or markdown (.md)
- 🌐 **Web Interface**: Easy-to-use drag-and-drop web interface
- 🔄 **Background Processing**: Clean extraction without content modification
- 💾 **Download**: Direct download of converted files
- 🗑️ **Cleanup**: Built-in file cleanup functionality

## Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/epub-converter.git
cd epub-converter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and go to `http://localhost:5000`

## Usage

### Web Interface

1. Open the web interface at `http://localhost:5000`
2. Drag and drop your EPUB file or click to browse
3. Select output format (Text or Markdown)
4. Click "Convert EPUB"
5. Download your converted file

### Command Line

You can also use the converter directly from the command line:

```bash
# Convert to text
python epub_converter.py book.epub txt

# Convert to markdown
python epub_converter.py book.epub md
```

## File Structure

```
epub-converter/
├── app.py                 # Flask web application
├── epub_converter.py      # Core conversion logic
├── requirements.txt       # Python dependencies
├── templates/
│   ├── index.html        # Upload page
│   └── result.html       # Download page
├── uploads/              # Temporary upload storage
└── outputs/              # Converted files storage
```

## Dependencies

- **ebooklib**: EPUB file reading and parsing
- **beautifulsoup4**: HTML content parsing
- **flask**: Web framework for the interface
- **lxml**: XML parsing support
- **markdownify**: HTML to Markdown conversion

## Technical Details

### Conversion Process

1. **EPUB Reading**: Uses `ebooklib` to read and parse EPUB files
2. **Content Extraction**: Extracts HTML content from each chapter/section
3. **Text Processing**: Cleans up HTML and converts to desired format
4. **Structure Preservation**: Maintains chapter structure and formatting
5. **File Generation**: Creates clean text or markdown output

### Supported Features

- ✅ Text extraction from all EPUB chapters
- ✅ HTML to text/markdown conversion
- ✅ Chapter structure preservation
- ✅ Author and title metadata
- ✅ Clean formatting output
- ✅ Special character handling

## Configuration

The application includes several configurable options in `app.py`:

- **MAX_CONTENT_LENGTH**: Maximum file size (default: 50MB)
- **UPLOAD_FOLDER**: Temporary upload directory
- **OUTPUT_FOLDER**: Converted files directory

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Troubleshooting

### Common Issues

- **Large files**: Ensure your EPUB file is under 50MB
- **Corrupt EPUB**: Verify your EPUB file opens in other readers
- **Dependencies**: Make sure all requirements are installed correctly

### Getting Help

If you encounter issues:

1. Check the console output for error messages
2. Verify your Python version is 3.7+
3. Ensure all dependencies are installed
4. Try with a different EPUB file to isolate the issue

## Acknowledgments

- Built with [ebooklib](https://github.com/aerkalov/ebooklib) for EPUB parsing
- Uses [Flask](https://flask.palletsprojects.com/) for the web interface
- Powered by [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML processing