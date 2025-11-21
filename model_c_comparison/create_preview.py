#!/usr/bin/env python3
"""
Create simple HTML preview of generated pages
(Alternative to Hugo for quick preview)
"""
import json
from pathlib import Path

def create_html_preview():
    """Generate standalone HTML files from JSON"""
    
    generated_dir = Path(__file__).parent / "generated"
    preview_dir = Path(__file__).parent / "preview"
    preview_dir.mkdir(exist_ok=True)
    
    # CSS template
    css = """
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        article {
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #1a1a1a;
        }
        h2 {
            font-size: 1.8em;
            margin: 30px 0 15px;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        h3 {
            font-size: 1.4em;
            margin: 25px 0 10px;
            color: #34495e;
        }
        h4 {
            font-size: 1.1em;
            margin: 15px 0 10px;
            color: #555;
        }
        .quick-answer {
            background: #e8f4f8;
            padding: 20px;
            border-left: 4px solid #3498db;
            margin: 20px 0;
            border-radius: 4px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background: #3498db;
            color: white;
            font-weight: 600;
        }
        tr:hover {
            background: #f8f9fa;
        }
        .btn, .cta-button {
            display: inline-block;
            padding: 10px 20px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background 0.3s;
        }
        .btn:hover, .cta-button:hover {
            background: #2980b9;
        }
        .btn-secondary {
            background: #95a5a6;
        }
        .btn-secondary:hover {
            background: #7f8c8d;
        }
        .pros-cons {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 20px 0;
        }
        .pros, .cons {
            padding: 15px;
            border-radius: 5px;
        }
        .pros {
            background: #d5f4e6;
            border-left: 4px solid #27ae60;
        }
        .cons {
            background: #fadbd8;
            border-left: 4px solid #e74c3c;
        }
        ul {
            margin-left: 20px;
            margin-top: 10px;
        }
        li {
            margin: 8px 0;
        }
        .disclaimer {
            background: #fff3cd;
            padding: 20px;
            border-radius: 5px;
            border-left: 4px solid #ffc107;
            margin: 30px 0;
        }
        .disclaimer-box {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-top: 10px;
        }
        footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #777;
            font-size: 0.9em;
        }
        .faq-item {
            margin: 20px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 5px;
        }
        .updated {
            color: #777;
            font-size: 0.9em;
            margin-bottom: 20px;
        }
        .lead {
            font-size: 1.2em;
            color: #555;
            margin: 15px 0;
        }
        @media (max-width: 768px) {
            .pros-cons {
                grid-template-columns: 1fr;
            }
            body {
                padding: 10px;
            }
            article {
                padding: 20px;
            }
        }
    </style>
    """
    
    json_files = list(generated_dir.glob("*.json"))
    
    if not json_files:
        print("❌ No generated JSON files found")
        return []
    
    html_files = []
    
    for json_file in json_files:
        with open(json_file) as f:
            data = json.load(f)
        
        # Create HTML
        html = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{data['meta_description']}">
    <title>{data['title']}</title>
    {css}
</head>
<body>
    {data['html_content']}
</body>
</html>
"""
        
        # Save HTML
        html_filename = json_file.stem + '.html'
        html_file = preview_dir / html_filename
        
        with open(html_file, 'w') as f:
            f.write(html)
        
        print(f"✅ Created: {html_filename}")
        html_files.append(html_file)
    
    # Create index
    index_html = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CryptoCompare - Preview</title>
    {css}
</head>
<body>
    <article>
        <h1>🚀 CryptoCompare Preview</h1>
        <p class="lead">Generated comparison pages ready for review</p>
        
        <h2>📄 Pages ({len(html_files)})</h2>
        <ul>
"""
    
    for html_file in html_files:
        title = html_file.stem.replace('_', ' ').title()
        index_html += f'            <li><a href="{html_file.name}">{title}</a></li>\n'
    
    index_html += """
        </ul>
        
        <h2>✅ Next Steps</h2>
        <ol>
            <li>Review pages above</li>
            <li>Install Hugo: <code>brew install hugo</code></li>
            <li>Run: <code>python3 build_site.py</code></li>
            <li>Deploy to Cloudflare Pages</li>
        </ol>
    </article>
</body>
</html>
"""
    
    index_file = preview_dir / 'index.html'
    with open(index_file, 'w') as f:
        f.write(index_html)
    
    print(f"\n✅ Created index: {index_file}")
    
    return html_files, index_file

if __name__ == "__main__":
    print("📄 Creating HTML preview...")
    print("=" * 60)
    
    html_files, index_file = create_html_preview()
    
    print("=" * 60)
    print(f"\n✅ Preview ready! Open in browser:")
    print(f"\n   file://{index_file.absolute()}")
    print(f"\nor:")
    print(f"   open {index_file}")
