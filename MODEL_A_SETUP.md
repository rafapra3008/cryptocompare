# 🗄️ B) MODEL A SETUP - PriceIntel Infrastructure

**Time:** 3 hours  
**Goal:** Domain live, database ready, 20 pages published  
**Site:** cryptoprice-live.com

---

## PHASE 1: Domain Purchase (30 min)

### Step 1: Buy Domain on Cloudflare

1. **Go to:** https://dash.cloudflare.com
2. **Domain Registrar** → **Register Domain**
3. **Search:** `cryptoprice-live.com`
4. **Check availability** (if taken, try: crypto-price-live.com, livecryptoprice.com)
5. **Purchase:** €10-12/year
6. **Privacy:** Auto-enabled
7. **Confirm purchase**

### Step 2: Vercel Project Setup

1. **Go to:** https://vercel.com/dashboard
2. **New Project** → **Import Git Repository**
3. **Select:** revenue_portfolio repo
4. **Project name:** `priceint el`
5. **Root directory:** `model_a_pricetracker`
6. **Build settings:**
   ```
   Build Command: cd site && hugo --minify
   Output Directory: site/public
   Install Command: (leave default)
   ```

7. **Environment Variables:**
   ```
   HUGO_VERSION=0.152.2
   ```

8. **Deploy!**

### Step 3: Custom Domain

1. **Vercel project** → **Settings** → **Domains**
2. **Add:** `cryptoprice-live.com`
3. **Select:** Production
4. **Cloudflare auto-configures DNS** ✅
5. **Wait 2-5 min** → SSL active!

---

## PHASE 2: Database Setup (60 min)

### Option A: Railway (Recommended - Free tier)

**Setup:**
1. **Go to:** https://railway.app
2. **New Project** → **Provision PostgreSQL**
3. **Free tier:** 500MB, $5 credit
4. **Get connection string:**
   ```
   postgresql://user:password@host:port/database
   ```

5. **Save to `.env`:**
   ```bash
   DATABASE_URL=postgresql://...
   ```

### Option B: Supabase (Alternative - Free tier)

1. **Go to:** https://supabase.com
2. **New project** → **Create database**
3. **Free tier:** 500MB, 2 projects
4. **Connection pooler** → Get URL

### Run Schema

**In your terminal:**

```bash
cd /Users/rafapra/.gemini/antigravity/scratch/revenue_portfolio

# Test connection
psql $DATABASE_URL

# Run schema
psql $DATABASE_URL < shared/schema.sql

# Verify tables
psql $DATABASE_URL -c "\dt"
```

**Expected output:**
```
             List of relations
 Schema |       Name        | Type  |  Owner   
--------+-------------------+-------+----------
 public | exchanges         | table | postgres
 public | prices            | table | postgres
 public | price_history     | table | postgres
```

### Populate Initial Data

**Add exchanges:**

```bash
psql $DATABASE_URL << SQL
INSERT INTO exchanges (id, name, url) VALUES 
  ('binance', 'Binance', 'https://binance.com'),
  ('coinbase', 'Coinbase', 'https://coinbase.com'),
  ('kraken', 'Kraken', 'https://kraken.com'),
  ('crypto_com', 'Crypto.com', 'https://crypto.com');
SQL
```

**First price fetch:**

```bash
python3 scripts/fetch_prices.py
```

**Verify:**
```bash
psql $DATABASE_URL -c "SELECT * FROM prices LIMIT 5;"
```

---

## PHASE 3: Hugo Site (60 min)

### Create Site Structure

**If not exists:**

```bash
cd model_a_pricetracker
mkdir -p site

cd site
hugo new site . --force

# Directory structure:
# site/
# ├── content/
# ├── layouts/
# ├── static/
# └── hugo.toml
```

### Configure Hugo

**Edit `hugo.toml`:**

```toml
baseURL = 'https://cryptoprice-live.com/'
languageCode = 'en-us'
title = 'Crypto Price Live - Real-time Cryptocurrency Prices'
theme = ''

[params]
  description = 'Live cryptocurrency prices, charts, and historical data for Bitcoin, Ethereum, and 1000+ coins'

[[menus.main]]
  name = 'Home'
  url = '/'
  weight = 1

[[menus.main]]
  name = 'Bitcoin'
  url = '/prices/bitcoin-usd/'
  weight = 2

[[menus.main]]
  name = 'Ethereum'
  url = '/prices/ethereum-usd/'
  weight = 3
```

### Create Layout (Green Theme)

**Create `layouts/_default/baseof.html`:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ .Title }} | {{ .Site.Title }}</title>
    <meta name="description" content="{{ .Description }}">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }
        header {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 20px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 0 20px;
        }
        main {
            background: white;
            margin: 30px auto;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            max-width: 900px;
        }
        h1 { font-size: 2.5em; color: #1a1a1a; margin-bottom: 20px; }
        .price-box {
            background: linear-gradient(135deg, #10b98122 0%, #05966922 100%);
            padding: 30px;
            border-radius: 8px;
            text-align: center;
            margin: 30px 0;
        }
        .price { font-size: 3em; color: #059669; font-weight: bold; }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>{{ .Site.Title }}</h1>
            <p>{{ .Site.Params.description }}</p>
        </div>
    </header>
    
    <main class="container">
        {{ block "main" . }}{{ end }}
    </main>
</body>
</html>
```

---

## PHASE 4: Generate First 20 Pages (30 min)

### Create Generation Script

**Create `model_a_pricetracker/generate_pages.py`:**

```python
#!/usr/bin/env python3
import os
from datetime import datetime

# Top 20 price pages
pages = [
    ("bitcoin-usd", "Bitcoin Price USD", "BTC", "USD"),
    ("bitcoin-eur", "Bitcoin Price EUR", "BTC", "EUR"),
    ("ethereum-usd", "Ethereum Price USD", "ETH", "USD"),
    ("ethereum-eur", "Ethereum Price EUR", "ETH", "EUR"),
    ("bitcoin-gbp", "Bitcoin Price GBP", "BTC", "GBP"),
    ("ethereum-gbp", "Ethereum Price GBP", "ETH", "GBP"),
    ("litecoin-usd", "Litecoin Price USD", "LTC", "USD"),
    ("ripple-usd", "Ripple (XRP) Price USD", "XRP", "USD"),
    ("cardano-usd", "Cardano (ADA) Price USD", "ADA", "USD"),
    ("solana-usd", "Solana Price USD", "SOL", "USD"),
    ("polkadot-usd", "Polkadot Price USD", "DOT", "USD"),
    ("dogecoin-usd", "Dogecoin Price USD", "DOGE", "USD"),
    ("avalanche-usd", "Avalanche Price USD", "AVAX", "USD"),
    ("polygon-usd", "Polygon Price USD", "MATIC", "USD"),
    ("chainlink-usd", "Chainlink Price USD", "LINK", "USD"),
    ("uniswap-usd", "Uniswap Price USD", "UNI", "USD"),
    ("bitcoin-cad", "Bitcoin Price CAD", "BTC", "CAD"),
    ("ethereum-cad", "Ethereum Price CAD", "ETH", "CAD"),
    ("bitcoin-aud", "Bitcoin Price AUD", "BTC", "AUD"),
    ("ethereum-aud", "Ethereum Price AUD", "ETH", "AUD"),
]

os.makedirs("site/content/prices", exist_ok=True)

for slug, title, coin, currency in pages:
    content = f'''---
title: "{title} - Live Chart & Price Today"
description: "Real-time {coin}/{currency} price, 24h chart, historical data. Updated every minute."
date: {datetime.now().isoformat()}
keywords: ["{coin} price", "{coin} {currency}", "{coin} live price"]
draft: false
---

<article>
    <h1>{title}</h1>
    
    <div class="price-box">
        <div class="price" id="current-price">Loading...</div>
        <p>Last updated: <span id="last-update">...</span></p>
    </div>
    
    <h2>About {coin}</h2>
    <p>{coin} price in {currency} updates every minute. Track live price, 24h change, and historical charts.</p>
    
    <h2>24h Price Change</h2>
    <p>Coming soon: Interactive 24-hour price chart</p>
    
    <h2>Where to Buy {coin}</h2>
    <ul>
        <li><strong>Binance:</strong> Low fees (0.1%), high liquidity</li>
        <li><strong>Coinbase:</strong> Beginner-friendly, regulated</li>
        <li><strong>Kraken:</strong> Advanced trading, good support</li>
    </ul>
    
    <p><a href="https://www.cryptoverso2025.com/comparisons/best-crypto-exchange-italy-2025/">Compare all exchanges →</a></p>
</article>

<script>
// TODO: Fetch live price from API
document.getElementById('current-price').textContent = '${currency} ...';
document.getElementById('last-update').textContent = new Date().toLocaleString();
</script>
'''
    
    with open(f"site/content/prices/{slug}.md", "w") as f:
        f.write(content)
    
    print(f"✅ Created: {slug}.md")

print(f"\n🎉 Generated {len(pages)} pages!")
```

### Generate & Deploy

```bash
cd model_a_pricetracker
python3 generate_pages.py

cd site
hugo --minify

# Test locally
hugo server -D

# Deploy
cd ../..
git add model_a_pricetracker/
git commit -m "🚀 Model A: First 20 price pages"
git push

# Vercel auto-deploys!
```

### Verify Live

**Check these URLs work:**
- https://cryptoprice-live.com/
- https://cryptoprice-live.com/prices/bitcoin-usd/
- https://cryptoprice-live.com/prices/ethereum-usd/

---

## ✅ SUCCESS CHECKLIST

**Phase 1:**
- [ ] Domain purchased (cryptoprice-live.com)
- [ ] Vercel project created
- [ ] Custom domain configured
- [ ] SSL active (HTTPS working)

**Phase 2:**
- [ ] Database provisioned (Railway/Supabase)
- [ ] Schema deployed
- [ ] Exchanges added
- [ ] First prices fetched

**Phase 3:**
- [ ] Hugo site created
- [ ] Green gradient theme
- [ ] Layouts working
- [ ] Test build successful

**Phase 4:**
- [ ] 20 pages generated
- [ ] Deployed to Vercel
- [ ] All pages accessible
- [ ] Cross-links to Model C working

---

## 📊 EXPECTED RESULTS

**Immediate:**
- Model A live at cryptoprice-live.com
- 20 SEO-optimized pages
- Database infrastructure ready

**Week 1:**
- Google starts crawling
- First indexed pages
- Cross-traffic from Model C

**Month 1:**
- 100+ pages total
- First organic traffic
- AdSense application

---

**TOTAL TIME: 3 hours**  
**INVESTMENT: €10 (domain)**  
**OUTPUT: Full infrastructure + 20 pages!** 🚀💙

**START WITH DOMAIN PURCHASE NOW!**
