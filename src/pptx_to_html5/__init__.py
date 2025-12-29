"""PowerPoint to HTML5 conversion tools."""

from importlib.metadata import version as get_version

from pptx_to_html5.converter import PowerPointToHTML5Converter

__version__ = get_version(__package__) # type: ignore
__all__ = ["PowerPointToHTML5Converter"]
