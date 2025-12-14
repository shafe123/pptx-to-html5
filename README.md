# pptx_tools

A Python tool for converting PowerPoint presentations (.pptx) to interactive HTML5 websites.

## Features

- 🎨 Convert PowerPoint presentations to standalone HTML5 websites
- 📱 Responsive design that works on desktop and mobile devices
- ⌨️ Keyboard navigation (arrow keys, space, Home, End)
- 👆 Touch/swipe support for mobile devices
- 📝 Optional speaker notes inclusion
- 🎯 Clean, modern UI with smooth transitions
- 🔄 Progress bar and slide counter
- 💻 Command-line interface for easy automation

## Requirements

- Python 3.12 or higher
- Dependencies: python-pptx, Pillow, Jinja2

## Installation

### From source

```bash
git clone https://github.com/shafe123/pptx_tools.git
cd pptx_tools
pip install -e .
```

### Development installation

```bash
pip install -e ".[dev]"
```

## Usage

### Command Line

Convert a PowerPoint presentation to HTML5:

```bash
pptx-to-html presentation.pptx
```

Specify an output directory:

```bash
pptx-to-html presentation.pptx -o output_folder
```

Include speaker notes in the output:

```bash
pptx-to-html presentation.pptx --include-notes
```

### Python API

```python
from pptx_tools.converter import PowerPointToHTML5Converter

# Create converter
converter = PowerPointToHTML5Converter("presentation.pptx")

# Convert to HTML5
output_path = converter.convert("output_folder", include_notes=False)

print(f"Presentation converted to: {output_path}")
```

## Output Structure

The converter creates a self-contained website with:

- `index.html` - Main presentation file
- `styles.css` - Styling and layout
- `script.js` - Navigation and interactivity

Simply open `index.html` in any modern web browser to view the presentation.

## Navigation Controls

- **Arrow Keys** (← →): Navigate between slides
- **Space Bar**: Next slide
- **Home**: Go to first slide
- **End**: Go to last slide
- **Mouse/Touch**: Use on-screen buttons or swipe gestures

## Development

### Running Tests

```bash
pytest
```

### Code Quality

The project follows PEP8 style guidelines and uses type hints throughout.

Run linting:

```bash
ruff check src/
```

Run type checking:

```bash
mypy src/
```

## License

This is free and unencumbered software released into the public domain - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.