# Copilot Instructions for pptx_tools Project

## Project Overview

This project provides tools for converting PowerPoint presentations to HTML5 websites. The codebase follows modern Python best practices with strict type checking, PEP8 compliance, and comprehensive testing.

## Project Structure

```
pptx_tools/
├── src/pptx_tools/          # Main source code
│   ├── __init__.py          # Package initialization
│   ├── converter.py         # Core PowerPointToHTML5Converter class
│   └── cli.py               # Command-line interface
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── test_converter.py    # Tests for converter module
│   └── test_cli.py          # Tests for CLI module
├── pyproject.toml           # Project configuration, dependencies, and tool settings
├── README.md                # User documentation
└── .gitignore               # Git ignore patterns
```

## Code Standards

### Python Version
- **Minimum**: Python 3.12
- **Target**: Python 3.13+ (when available)
- Use modern Python features like `|` union types (e.g., `str | Path`)

### Type Hints
- **ALWAYS** include type hints on all functions and methods
- Use strict typing: `-> None`, `-> str`, etc.
- Follow mypy strict mode requirements
- Import types from `typing` or use built-in types (Python 3.10+)

### Code Style
- Follow **PEP8** guidelines strictly
- Line length: **88 characters** (ruff default)
- Use descriptive variable names
- Add docstrings to all public functions/classes (Google style)
- Use f-strings for string formatting

### Linting and Type Checking
```bash
# Run linter (should pass with no errors)
ruff check src/ tests/

# Auto-fix linting issues
ruff check --fix src/ tests/

# Run type checker (should pass with no errors)
mypy src/pptx_tools/
```

### Testing
```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_converter.py -v

# Check coverage
pytest --cov=pptx_tools --cov-report=term-missing
```

**Test Requirements:**
- Maintain **>90% code coverage**
- Use pytest fixtures for test data
- Clean up resources (use `yield` fixtures for cleanup)
- Test both success and error cases
- Use descriptive test names: `test_<function>_<scenario>`

## Dependencies

### Core Dependencies
- `python-pptx>=0.6.21` - Reading PowerPoint files
- `Pillow>=10.2.0` - Image processing (NOTE: Use >=10.2.0 for security)
- `Jinja2>=3.1.0` - HTML templating

### Development Dependencies
- `pytest>=7.4.0` - Testing framework
- `pytest-cov>=4.1.0` - Coverage reporting
- `ruff>=0.1.0` - Linting
- `mypy>=1.5.0` - Type checking

## Making Code Changes

### Adding New Features
1. **Write tests first** (TDD approach preferred)
2. Implement the feature with type hints
3. Update docstrings
4. Run linter and type checker
5. Ensure tests pass with good coverage
6. Update README if user-facing

### Modifying Existing Code
1. Understand the existing tests
2. Add tests for new behavior
3. Make minimal changes
4. Verify all tests still pass
5. Check linting and type checking
6. Update documentation if needed

### Common Patterns

#### Creating a new converter method:
```python
def _extract_something(self, slide: Slide) -> dict[str, Any]:
    """Extract something from a slide.
    
    Args:
        slide: The slide to process
        
    Returns:
        Dictionary containing extracted data
    """
    result: dict[str, Any] = {}
    # Implementation
    return result
```

#### CLI argument handling:
```python
parser.add_argument(
    "--option",
    type=str,
    default=None,
    help="Description of the option",
)
```

## HTML/CSS/JavaScript

The converter generates three files:
- `index.html` - HTML5 structure (uses Jinja2 templates)
- `styles.css` - Modern, responsive CSS
- `script.js` - Navigation and interactivity

### HTML Template Guidelines
- Use semantic HTML5 elements
- Include proper meta tags
- Use data attributes for JavaScript hooks
- Keep templates clean and readable

### CSS Guidelines
- Mobile-first responsive design
- Use CSS custom properties for theming
- Modern flexbox/grid layouts
- Smooth transitions and animations

### JavaScript Guidelines
- Vanilla JavaScript (no jQuery)
- Use modern ES6+ features
- Event delegation where appropriate
- Support keyboard and touch navigation

## Security Considerations

1. **Input Validation**: Always validate PowerPoint file paths and formats
2. **Path Traversal**: Use `Path` objects, avoid string concatenation
3. **Dependencies**: Keep dependencies updated (especially Pillow for security fixes)
4. **HTML Output**: Jinja2 auto-escapes by default - don't disable it
5. **File Cleanup**: Always clean up temporary files in tests

## Debugging

### Running the CLI locally:
```bash
# After installing in editable mode
pip install -e .

# Convert a presentation
pptx-to-html sample.pptx -o output/

# With notes
pptx-to-html sample.pptx --include-notes
```

### Python API usage:
```python
from pptx_tools.converter import PowerPointToHTML5Converter

converter = PowerPointToHTML5Converter("presentation.pptx")
output_path = converter.convert("output_dir", include_notes=False)
```

## Git Workflow

1. Make changes in small, focused commits
2. Write descriptive commit messages
3. Ensure tests pass before committing
4. Keep sample/demo files out of the repo (use .gitignore)

## Common Issues and Solutions

### Issue: Linting fails with line length
**Solution**: Break long lines, especially in templates. E501 is ignored for embedded templates.

### Issue: Tests fail due to temp files
**Solution**: Use yield fixtures for cleanup. See `tests/test_converter.py` for examples.

### Issue: Type checking fails
**Solution**: Ensure all functions have type hints. Use `-> None` for void functions.

### Issue: Import errors
**Solution**: Install package in editable mode: `pip install -e .`

## Future Enhancements

Potential areas for improvement:
1. **Actual slide rendering** - Currently uses placeholder images. Could integrate LibreOffice or other rendering engines.
2. **Themes** - Multiple CSS themes for different presentation styles
3. **Animations** - Support for PowerPoint animations
4. **Export formats** - PDF, images, etc.
5. **Slide transitions** - Animated transitions between slides
6. **Progressive Web App** - Make presentations work offline

## Questions?

Refer to:
- README.md for user documentation
- pyproject.toml for configuration
- Existing tests for examples
- PEP8 and Python documentation for style questions
