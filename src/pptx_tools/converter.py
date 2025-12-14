"""Core PowerPoint to HTML5 converter."""

import base64
import io
from pathlib import Path
from typing import Any

from jinja2 import Template
from PIL import Image
from pptx import Presentation
from pptx.slide import Slide


class PowerPointToHTML5Converter:
    """Convert PowerPoint presentations to HTML5 websites."""

    def __init__(self, pptx_path: str | Path) -> None:
        """Initialize the converter with a PowerPoint file.

        Args:
            pptx_path: Path to the PowerPoint file (.pptx)

        Raises:
            FileNotFoundError: If the PowerPoint file doesn't exist
            ValueError: If the file is not a valid PowerPoint file
        """
        self.pptx_path = Path(pptx_path)
        if not self.pptx_path.exists():
            raise FileNotFoundError(f"File not found: {pptx_path}")
        if not self.pptx_path.suffix.lower() == ".pptx":
            raise ValueError(f"File must be a .pptx file: {pptx_path}")

        try:
            self.presentation = Presentation(str(self.pptx_path))
        except Exception as e:
            raise ValueError(f"Invalid PowerPoint file: {e}") from e

        # Get path to templates directory
        self.templates_dir = Path(__file__).parent / "templates"

    def _slide_to_image(self, slide: Slide, slide_number: int) -> str:
        """Convert a slide to a base64-encoded PNG image.

        Args:
            slide: The slide to convert
            slide_number: The slide number (for identification)

        Returns:
            Base64-encoded PNG image as a data URI
        """
        # Create an image from the slide
        # Since python-pptx doesn't provide direct rendering, we'll export metadata
        # and use a placeholder approach. For production, you'd use a library like
        # aspose.slides or convert via LibreOffice/unoconv
        img = Image.new("RGB", (1280, 720), color=(255, 255, 255))

        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"

    def _extract_slide_content(self, slide: Slide) -> dict[str, Any]:
        """Extract text and content from a slide.

        Args:
            slide: The slide to extract content from

        Returns:
            Dictionary containing slide content
        """
        content: dict[str, Any] = {
            "title": "",
            "text": [],
            "notes": "",
        }

        # Extract text from shapes
        for shape in slide.shapes:
            if hasattr(shape, "text") and shape.text:
                text = shape.text.strip()
                if text:
                    # First text element is often the title
                    if not content["title"] and hasattr(shape, "text_frame"):
                        content["title"] = text
                    else:
                        content["text"].append(text)

        # Extract speaker notes
        if slide.has_notes_slide:
            notes_slide = slide.notes_slide
            if notes_slide.notes_text_frame:
                content["notes"] = notes_slide.notes_text_frame.text.strip()

        return content

    def convert(
        self, output_dir: str | Path, include_notes: bool = False
    ) -> Path:
        """Convert the PowerPoint presentation to an HTML5 website.

        Args:
            output_dir: Directory where the HTML5 website will be created
            include_notes: Whether to include speaker notes in the output

        Returns:
            Path to the generated index.html file

        Raises:
            OSError: If the output directory cannot be created
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Extract slides
        slides_data = []
        for i, slide in enumerate(self.presentation.slides):
            slide_content = self._extract_slide_content(slide)
            slide_data = {
                "number": i + 1,
                "image": self._slide_to_image(slide, i),
                "title": slide_content["title"],
                "text": slide_content["text"],
                "notes": slide_content["notes"] if include_notes else "",
            }
            slides_data.append(slide_data)

        # Generate HTML
        html_content = self._generate_html(slides_data, include_notes)
        html_path = output_path / "index.html"
        html_path.write_text(html_content, encoding="utf-8")

        # Generate CSS
        css_content = self._generate_css()
        css_path = output_path / "styles.css"
        css_path.write_text(css_content, encoding="utf-8")

        # Generate JavaScript
        js_content = self._generate_js()
        js_path = output_path / "script.js"
        js_path.write_text(js_content, encoding="utf-8")

        return html_path

    def _generate_html(
        self, slides_data: list[dict[str, Any]], include_notes: bool
    ) -> str:
        """Generate HTML content for the presentation.

        Args:
            slides_data: List of slide data dictionaries
            include_notes: Whether to include speaker notes

        Returns:
            HTML content as a string
        """
        template_path = self.templates_dir / "presentation.html"
        template_content = template_path.read_text(encoding="utf-8")
        template = Template(template_content)

        title = (
            slides_data[0]["title"]
            if slides_data and slides_data[0]["title"]
            else "Presentation"
        )

        return template.render(
            title=title, slides=slides_data, include_notes=include_notes
        )

    def _generate_css(self) -> str:
        """Generate CSS styles for the presentation.

        Returns:
            CSS content as a string
        """
        css_path = self.templates_dir / "styles.css"
        return css_path.read_text(encoding="utf-8")

    def _generate_js(self) -> str:
        """Generate JavaScript for slide navigation and interactivity.

        Returns:
            JavaScript content as a string
        """
        js_path = self.templates_dir / "script.js"
        return js_path.read_text(encoding="utf-8")
