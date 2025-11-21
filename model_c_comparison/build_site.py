"""
Build Hugo static site for Model C (CryptoCompare)
Generates pages from database and deploys
"""
import os
import sys
import json
from pathlib import Path
import logging

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from shared.db import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SITE_DIR = Path(__file__).parent / "site"
CONTENT_DIR = SITE_DIR / "content"

def init_hugo_site():
    """Initialize Hugo site if not exists"""
    if not SITE_DIR.exists():
        logger.info("Creating Hugo site...")
        os.system(f"hugo new site {SITE_DIR}")
        logger.info("✅ Hugo site created")
    else:
        logger.info("Hugo site already exists")

def create_comparison_page(page_data: dict):
    """
    Create a Hugo markdown page from generated content
    
    Args:
        page_data: Dict with title, meta_description, html_content, keyword
    """
    # Create slug from keyword
    slug = page_data['keyword'].lower().replace(' ', '-')
    
    # Hugo front matter (YAML)
    front_matter = f"""---
title: "{page_data['title']}"
description: "{page_data['meta_description']}"
date: {page_data.get('generated_at', '2025-11-22T00:00:00Z')}
keywords: ["{page_data['keyword']}", "crypto exchange", "comparison"]
draft: false
type: "comparison"
layout: "single"
---

{page_data['html_content']}
"""
    
    # Write to content directory
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = CONTENT_DIR / f"{slug}.md"
    
    with open(output_file, 'w') as f:
        f.write(front_matter)
    
    logger.info(f"✅ Created: {output_file}")
    
    # Also save to database
    try:
        db.execute_query(
            """
            INSERT INTO pages_comparison (slug, title, meta_description, content, keyword)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (slug) DO UPDATE SET
                content = EXCLUDED.content,
                updated_at = NOW()
            """,
            (slug, page_data['title'], page_data['meta_description'], 
             page_data['html_content'], page_data['keyword'])
        )
        logger.info(f"✅ Saved to database: {slug}")
    except Exception as e:
        logger.warning(f"Database save failed: {e}")

def build_site():
    """Build Hugo static site"""
    logger.info("Building Hugo site...")
    os.chdir(SITE_DIR)
    result = os.system("hugo --minify")
    
    if result == 0:
        logger.info("✅ Site built successfully!")
        logger.info(f"Output: {SITE_DIR / 'public'}")
    else:
        logger.error("❌ Hugo build failed")
        return False
    
    return True

def deploy_cloudflare():
    """Deploy to Cloudflare Pages"""
    logger.info("Deploying to Cloudflare Pages...")
    
    # Cloudflare Pages deployment (requires wrangler CLI)
    # Install: npm install -g wrangler
    
    public_dir = SITE_DIR / "public"
    
    if not public_dir.exists():
        logger.error("❌ No public directory. Run build first.")
        return False
    
    # Deploy command
    cmd = f"npx wrangler pages deploy {public_dir} --project-name=cryptoexchange-compare"
    
    logger.info(f"Running: {cmd}")
    result = os.system(cmd)
    
    if result == 0:
        logger.info("✅ Deployed to Cloudflare Pages!")
    else:
        logger.error("❌ Deployment failed")
        logger.info("Tip: Install wrangler: npm install -g wrangler")
        logger.info("Then login: wrangler login")
    
    return result == 0

def main():
    """Main build & deploy pipeline"""
    logger.info("🚀 Model C Build Pipeline")
    logger.info("=" * 50)
    
    # Step 1: Init Hugo
    init_hugo_site()
    
    # Step 2: Check for generated pages
    generated_dir = Path(__file__).parent / "generated"
    
    if not generated_dir.exists() or not list(generated_dir.glob("*.json")):
        logger.warning("⚠️  No generated pages found in generated/")
        logger.info("Run: python3 generate_content.py first")
        return
    
    # Step 3: Create Hugo pages from generated content
    logger.info(f"\nProcessing generated pages from {generated_dir}...")
    
    for json_file in generated_dir.glob("*.json"):
        with open(json_file) as f:
            page_data = json.load(f)
        
        create_comparison_page(page_data)
    
    # Step 4: Build site
    if not build_site():
        return
    
    # Step 5: Deploy (optional)
    deploy = input("\nDeploy to Cloudflare Pages? (y/N): ").lower()
    if deploy == 'y':
        deploy_cloudflare()
    else:
        logger.info("Skipping deployment")
        logger.info(f"Site ready at: {SITE_DIR / 'public' / 'index.html'}")
        logger.info("Test locally: cd site && hugo server")

if __name__ == "__main__":
    main()
