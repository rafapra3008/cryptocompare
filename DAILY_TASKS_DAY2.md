## Day 2 (Friday, Nov 22) - DEPLOYMENT DAY 🚀

**Objective:** Deploy to production + get API keys  
**Time Allocated:** 2-3 hours

### Morning Tasks (30 min) - DO FIRST!
- [ ] Buy domain: `cryptoexchange-compare.com` (Cloudflare, €12/year)
- [ ] Sign up for affiliate programs:
  - [ ] Binance: https://www.binance.com/en/activity/affiliate
  - [ ] Coinbase: https://www.coinbase.com/affiliates
  - [ ] Kraken: https://support.kraken.com/hc/en-us/articles/360027545252
- [ ] Get OpenRouter API key: https://openrouter.ai/
- [ ] Populate `.env` file with API keys and affiliate IDs
  ```bash
  cd /Users/rafapra/.gemini/antigravity/scratch/revenue_portfolio
  cp .env.example .env
  nano .env  # Add API keys
  ```

### Afternoon Tasks (2 hours)
- [ ] Generate REAL pages with GPT-4:
  ```bash
  cd model_c_comparison
  python3 generate_content.py
  ```
- [ ] Build Hugo site:
  ```bash
  cd site
  hugo -D
  ```
- [ ] Push to GitHub:
  ```bash
  git remote add origin https://github.com/YOUR_USERNAME/revenue-portfolio.git
  git push -u origin main
  ```
- [ ] Deploy to Cloudflare Pages:
  - [ ] Connect GitHub repo to Cloudflare Pages
  - [ ] Configure build: `hugo -D`
  - [ ] Set publish directory: `model_c_comparison/site/public`
  - [ ] Deploy!
- [ ] Configure domain DNS
- [ ] Enable SSL (automatic with Cloudflare)

### Evening Tasks
- [ ] Submit sitemap to Google Search Console
- [ ] Set up basic analytics (Plausible or Google Analytics)
- [ ] Test all 5 pages on production
- [ ] Request indexing for top 5 pages in GSC

**End of Day 2 Goal:**
- ✅ 5 pages LIVE on cryptoexchange-compare.com
- ✅ Affiliate tracking active
- ✅ Submitted to Google
- ✅ SSL enabled
- ✅ Code on GitHub

---
