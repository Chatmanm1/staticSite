# generate_rss.py

import os
from datetime import datetime
from email.utils import formatdate

# --- Configuration ---
# You must change this to your website's URL
SITE_URL = "https://matchamakes.net"
POSTS_DIR = "blogposts" # Changed from "posts" to "blogposts"
RSS_FILE = "rss.xml"

def get_post_info(filepath):
    """
    Extracts title and modification date from an HTML file.
    The title is assumed to be the filename without the extension.
    The date is the file's last modification time.
    """
    filename = os.path.basename(filepath)
    title = os.path.splitext(filename)[0].replace('-', ' ').replace('_', ' ').title()
    mtime = os.path.getmtime(filepath)
    pub_date = formatdate(mtime, localtime=False, usegmt=True)
    link = f"{SITE_URL}/{POSTS_DIR}/{filename}"
    return title, link, pub_date

def generate_rss():
    """Generates the rss.xml file."""
    
    # Get all html files from the posts directory, sorted by modification time (newest first)
    post_files = [os.path.join(POSTS_DIR, f) for f in os.listdir(POSTS_DIR) if f.endswith('.html')]
    post_files.sort(key=lambda f: os.path.getmtime(f), reverse=True)
    
    # Start building the RSS XML string
    rss_items = []
    for filepath in post_files:
        title, link, pub_date = get_post_info(filepath)
        rss_items.append(f"""
    <item>
      <title>{title}</title>
      <link>{link}</link>
      <guid isPermaLink="true">{link}</guid>
      <pubDate>{pub_date}</pubDate>
      <description>Read the post: {title}</description>
    </item>""")

    # Combine all parts into the final XML file
    rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>Matcha Makes</title>
  <link>{SITE_URL}</link>
  <description>Latest updates from Matcha Makes</description>
  <language>en-us</language>
  <lastBuildDate>{formatdate(usegmt=True)}</lastBuildDate>
  <atom:link href="{SITE_URL}/{RSS_FILE}" rel="self" type="application/rss+xml" />
  {''.join(rss_items)}
</channel>
</rss>
"""
    
    # Write the content to the RSS file
    with open(RSS_FILE, 'w', encoding='utf-8') as f:
        f.write(rss_content.strip())

    print(f"✅ Successfully generated {RSS_FILE} with {len(rss_items)} items.")

if __name__ == "__main__":
    generate_rss()
