#!/usr/bin/env python3
"""
Convert HTML-in-markdown comparison pages to pure markdown format.
Fixes the issue where HTML tags are visible as text instead of being rendered.
"""

import os
import re
from pathlib import Path

# Directory containing comparison pages
COMPARISONS_DIR = Path("/Users/rafapra/.gemini/antigravity/scratch/revenue_portfolio/model_c_comparison/site/content/comparisons")

def html_to_markdown(content):
    """Convert HTML markup to markdown syntax."""
    
    # Remove <article> tags
    content = re.sub(r'<article[^>]*>|</article>', '', content)
    
    # Remove <section> tags
    content = re.sub(r'<section[^>]*>|</section>', '', content)
    
    # Remove <div> tags
    content = re.sub(r'<div[^>]*>|</div>', '', content)
    
    # Remove <footer> tags
    content = re.sub(r'<footer>|</footer>', '', content)
    
    # Convert <h1> to #
    content = re.sub(r'<h1>(.*?)</h1>', r'# \1', content)
    
    # Convert <h2> to ##
    content = re.sub(r'<h2>(.*?)</h2>', r'## \1', content)
    
    # Convert <h3> to ###
    content = re.sub(r'<h3>(.*?)</h3>', r'### \1', content)
    
    # Convert <p><strong>...</strong></p> to **...**
    content =re.sub(r'<p><strong>(.*?)</strong>(.*?)</p>', r'**\1**\2\n', content)
    
    # Convert remaining <p> to plain text with newline
    content = re.sub(r'<p>(.*?)</p>', r'\1\n', content)
    
    # Convert <em> to *italics*
    content = re.sub(r'<em>(.*?)</em>', r'*\1*', content)
    
    # Convert <strong> to **bold** (if not already done)
    content = re.sub(r'<strong>(.*?)</strong>', r'**\1**', content)
    
    # Convert HTML table to markdown table
    content = convert_html_table_to_markdown(content)
    
    # Clean up extra blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content.strip()

def convert_html_table_to_markdown(content):
    """Convert HTML tables to markdown table syntax."""
    
    # Check if content has a table
    if '<table>' not in content:
        return content
    
    # Extract table section
    table_match = re.search(r'<table>.*?</table>', content, re.DOTALL)
    if not table_match:
        return content
    
    table_html = table_match.group(0)
    
    # Extract headers
    header_match = re.search(r'<thead>.*?</thead>', table_html, re.DOTALL)
    if header_match:
        headers = re.findall(r'<th>(.*?)</th>', header_match.group(0))
    else:
        # If no thead, check first tr
        first_tr = re.search(r'<tr>(.*?)</tr>', table_html, re.DOTALL)
        if first_tr:
            headers = re.findall(r'<th>(.*?)</th>', first_tr.group(0))
        else:
            return content  # Can't parse table
    
    # Extract rows from tbody
    tbody_match = re.search(r'<tbody>.*?</tbody>', table_html, re.DOTALL)
    if tbody_match:
        rows_html = tbody_match.group(0)
    else:
        # No tbody, get all tr after first
        rows_html = re.sub(r'<thead>.*?</thead>', '', table_html, flags=re.DOTALL)
    
    rows = re.findall(r'<tr>(.*?)</tr>', rows_html, re.DOTALL)
    
    # Build markdown table
    md_table = '| ' + ' | '.join(headers) + ' |\n'
    md_table += '|' + '|'.join(['--------'] * len(headers)) + '|\n'
    
    for row in rows:
        cells = re.findall(r'<td>(.*?)</td>', row, re.DOTALL)
        if cells:
            # Clean up cells (remove extra whitespace, keep HTML in links/buttons)
            cells = [cell.strip() for cell in cells]
            md_table += '| ' + ' | '.join(cells) + ' |\n'
    
    # Replace HTML table with markdown table
    result = content.replace(table_html, md_table)
    
    return result

def process_file(filepath):
    """Process a single markdown file."""
    print(f"Processing: {filepath.name}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split frontmatter and body
    parts = content.split('---', 2)
    if len(parts) >= 3:
        frontmatter = parts[1]
        body = parts[2]
    else:
        print(f"  ⚠️  No frontmatter found, skipping")
        return False
    
    # Convert body from HTML to markdown
    new_body = html_to_markdown(body)
    
    # Reconstruct file
    new_content = f"---{frontmatter}---\n\n{new_body}\n"
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✅ Converted successfully")
    return True

def main():
    """Main function to process all comparison files."""
    print("🔧 Converting HTML to Markdown in comparison pages...\n")
    
    if not COMPARISONS_DIR.exists():
        print(f"❌ Directory not found: {COMPARISONS_DIR}")
        return
    
    # Get all .md files
    md_files = list(COMPARISONS_DIR.glob('*.md'))
    
    print(f"Found {len(md_files)} markdown files\n")
    
    success_count = 0
    for filepath in md_files:
        if process_file(filepath):
            success_count += 1
        print()
    
    print(f"\n✅ Converted {success_count}/{len(md_files)} files successfully!")

if __name__ == '__main__':
    main()
