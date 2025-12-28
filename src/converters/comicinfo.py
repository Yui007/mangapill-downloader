"""
ComicInfo.xml generator for CBZ files.
Creates valid ComicInfo.xml with manga metadata.
"""

from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from typing import Optional

from ..scrapers.manga import MangaInfo, Chapter


def generate_comicinfo_xml(
    manga: MangaInfo,
    chapter: Optional[Chapter] = None,
    page_count: int = 0,
) -> str:
    """
    Generate ComicInfo.xml content for a CBZ file.
    
    Args:
        manga: MangaInfo object with manga metadata
        chapter: Optional Chapter object for chapter-specific info
        page_count: Number of pages in the chapter
        
    Returns:
        XML string for ComicInfo.xml
    """
    root = Element("ComicInfo")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
    
    # Title
    if chapter:
        SubElement(root, "Title").text = chapter.title
        SubElement(root, "Series").text = manga.title
        
        # Try to extract chapter number
        if chapter.number:
            try:
                num = float(chapter.number)
                SubElement(root, "Number").text = str(num)
            except ValueError:
                pass
    else:
        SubElement(root, "Title").text = manga.title
        SubElement(root, "Series").text = manga.title
    
    # Summary/Description
    if manga.description:
        SubElement(root, "Summary").text = manga.description
    
    # Year
    if manga.year:
        try:
            SubElement(root, "Year").text = str(int(manga.year))
        except ValueError:
            pass
    
    # Page count
    if page_count > 0:
        SubElement(root, "PageCount").text = str(page_count)
    
    # Genres
    if manga.genres:
        SubElement(root, "Genre").text = ", ".join(manga.genres)
    
    # Manga format indicator
    SubElement(root, "Manga").text = "Yes"
    
    # Type (if available)
    if manga.manga_type:
        SubElement(root, "Format").text = manga.manga_type
    
    # Status (Ongoing, Completed, etc.)
    if manga.status:
        if manga.status.lower() in ("completed", "finished"):
            SubElement(root, "Count").text = str(manga.chapters_count)
    
    # Web source
    SubElement(root, "Web").text = manga.url
    
    # Pretty print XML
    xml_string = tostring(root, encoding="unicode")
    parsed = minidom.parseString(xml_string)
    pretty_xml = parsed.toprettyxml(indent="  ")
    
    # Remove the XML declaration line for cleaner output
    lines = pretty_xml.split("\n")
    if lines[0].startswith("<?xml"):
        lines = lines[1:]
    
    return "\n".join(lines)


def create_comicinfo_element(name: str, value: str) -> Element:
    """
    Create a simple XML element with text content.
    
    Args:
        name: Element tag name
        value: Text content
        
    Returns:
        Element object
    """
    elem = Element(name)
    elem.text = value
    return elem
