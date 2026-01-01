#!/usr/bin/env python3
"""
Sitemap Generator Module - Generates XML sitemap for SEO.

Includes:
- Main sitemap.xml generation
- Archive page indexing
- Automatic lastmod timestamps
- Priority and changefreq settings
"""

from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import xml.etree.ElementTree as ET


def generate_sitemap(
    base_url: str = "https://dailytrending.info",
    archive_dates: Optional[List[str]] = None,
    public_dir: Optional[Path] = None
) -> str:
    """
    Generate XML sitemap for the website.

    Args:
        base_url: Base URL of the website
        archive_dates: List of archive dates (YYYY-MM-DD format)
        public_dir: Path to public directory to scan for archives

    Returns:
        XML string for sitemap.xml
    """
    # Create root element with namespace
    urlset = ET.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')

    today = datetime.now().strftime('%Y-%m-%d')

    # Add homepage (highest priority, updated daily)
    homepage = ET.SubElement(urlset, 'url')
    ET.SubElement(homepage, 'loc').text = f"{base_url}/"
    ET.SubElement(homepage, 'lastmod').text = today
    ET.SubElement(homepage, 'changefreq').text = 'daily'
    ET.SubElement(homepage, 'priority').text = '1.0'

    # Add archive index page
    archive_index = ET.SubElement(urlset, 'url')
    ET.SubElement(archive_index, 'loc').text = f"{base_url}/archive/"
    ET.SubElement(archive_index, 'lastmod').text = today
    ET.SubElement(archive_index, 'changefreq').text = 'daily'
    ET.SubElement(archive_index, 'priority').text = '0.8'

    # Add RSS feed
    rss_feed = ET.SubElement(urlset, 'url')
    ET.SubElement(rss_feed, 'loc').text = f"{base_url}/feed.xml"
    ET.SubElement(rss_feed, 'lastmod').text = today
    ET.SubElement(rss_feed, 'changefreq').text = 'daily'
    ET.SubElement(rss_feed, 'priority').text = '0.6'

    # Discover archive dates from public directory if not provided
    if archive_dates is None and public_dir:
        archive_dates = []
        archive_dir = public_dir / 'archive'
        if archive_dir.exists():
            for item in archive_dir.iterdir():
                if item.is_dir() and len(item.name) == 10:  # YYYY-MM-DD format
                    try:
                        datetime.strptime(item.name, '%Y-%m-%d')
                        archive_dates.append(item.name)
                    except ValueError:
                        continue

    # Add archive pages
    if archive_dates:
        for date in sorted(archive_dates, reverse=True):
            archive_page = ET.SubElement(urlset, 'url')
            ET.SubElement(archive_page, 'loc').text = f"{base_url}/archive/{date}/"
            ET.SubElement(archive_page, 'lastmod').text = date
            ET.SubElement(archive_page, 'changefreq').text = 'never'  # Archives don't change
            ET.SubElement(archive_page, 'priority').text = '0.5'

    # Convert to string with declaration
    xml_string = ET.tostring(urlset, encoding='unicode', method='xml')
    return f'<?xml version="1.0" encoding="UTF-8"?>\n{xml_string}'


def generate_robots_txt(base_url: str = "https://dailytrending.info") -> str:
    """
    Generate robots.txt with sitemap reference.

    Args:
        base_url: Base URL of the website

    Returns:
        robots.txt content string
    """
    return f"""# DailyTrending.info robots.txt
User-agent: *
Allow: /

# Sitemap location
Sitemap: {base_url}/sitemap.xml

# Disallow crawling of potential duplicate/utility paths
Disallow: /icons/
Disallow: /sw.js
"""


def save_sitemap(
    public_dir: Path,
    base_url: str = "https://dailytrending.info"
):
    """
    Save sitemap.xml and robots.txt to the public directory.

    Args:
        public_dir: Path to the public output directory
        base_url: Base URL of the website
    """
    # Generate and save sitemap
    sitemap_content = generate_sitemap(base_url=base_url, public_dir=public_dir)
    sitemap_path = public_dir / 'sitemap.xml'
    sitemap_path.write_text(sitemap_content)
    print(f"  Created {sitemap_path}")

    # Generate and save robots.txt
    robots_content = generate_robots_txt(base_url=base_url)
    robots_path = public_dir / 'robots.txt'
    robots_path.write_text(robots_content)
    print(f"  Created {robots_path}")

    print(f"SEO assets saved to {public_dir}")


def count_urls_in_sitemap(sitemap_path: Path) -> int:
    """
    Count the number of URLs in a sitemap.

    Args:
        sitemap_path: Path to sitemap.xml

    Returns:
        Number of URL entries
    """
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        # Handle namespace
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = root.findall('.//sm:url', ns)
        if not urls:
            # Try without namespace
            urls = root.findall('.//url')
        return len(urls)
    except Exception:
        return 0
