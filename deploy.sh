#!/bin/bash
# Quick deployment script for Cloudflare Pages
# Run after you have domain + API keys

set -e

echo "🚀 DEPLOYMENT SCRIPT - CryptoCompare"
echo "======================================"
echo ""

# Check we're in the right directory
if [ ! -f "DEPLOY_CHECKLIST.md" ]; then
    echo "❌ Error: Run this from revenue_portfolio root!"
    exit 1
fi

# Step 1: Generate real content with GPT-4 (if API key exists)
if [ -f ".env" ]; then
    source .env
    if [ -n "$OPENROUTER_API_KEY" ]; then
        echo "📝 Generating real GPT-4 content..."
        cd model_c_comparison
        python3 generate_content.py
        cd ..
        echo "✅ Content generated!"
    else
        echo "⚠️  No OpenRouter API key - using demo content"
    fi
else
    echo "⚠️  No .env file - using demo content"
fi

# Step 2: Build Hugo site
echo ""
echo "🏗️  Building Hugo site..."
cd model_c_comparison/site
hugo -D
cd ../..
echo "✅ Hugo build complete!"

# Step 3: Commit changes
echo ""
echo "📦 Committing to Git..."
git add -A
git commit -m "Production deployment - $(date '+%Y-%m-%d %H:%M')" || echo "No changes to commit"
echo "✅ Git commit done!"

# Step 4: Push to GitHub
echo ""
echo "⬆️  Pushing to GitHub..."
git push origin main
echo "✅ Pushed to GitHub!"

# Step 5: Info about Cloudflare
echo ""
echo "======================================"
echo "✅ BUILD COMPLETE!"
echo ""
echo "📊 Stats:"
ls -la model_c_comparison/site/public/ | wc -l | xargs echo "Files built:"
du -sh model_c_comparison/site/public/ | cut -f1 | xargs echo "Total size:"
echo ""
echo "🌐 Next Steps:"
echo "1. Go to: https://pages.cloudflare.com/"
echo "2. Click 'Create a project'"
echo "3. Connect to GitHub"
echo "4. Select: revenue-portfolio"
echo "5. Build settings:"
echo "   - Command: cd model_c_comparison/site && hugo -D"
echo "   - Output: model_c_comparison/site/public"
echo "6. Deploy!"
echo ""
echo "🎉 Site will be live in ~2 minutes!"
echo "======================================"
