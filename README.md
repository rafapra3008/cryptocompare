# CryptoCompare - Crypto Exchange Comparison Tool 🚀

**Automated revenue system comparing crypto exchanges for Italian market**

[![Deploy to Cloudflare Pages](https://img.shields.io/badge/Deploy-Cloudflare%20Pages-orange)](https://pages.cloudflare.com/)
[![Hugo](https://img.shields.io/badge/Built%20with-Hugo-ff4088)](https://gohugo.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Live Site:** Coming soon!

---

## 🎯 Project Goal

Generate **€5,000/month passive income** through SEO-optimized crypto exchange comparison pages with affiliate revenue.

**Revenue Model:**
- Binance Affiliate (50% commission)
- Coinbase Affiliate (€10/signup)
- Kraken Affiliate (20% commission)

**Target:** €2,000/month in 90 days → €5,000/month in 12 months

---

## ✨ Features

- 📊 **5 Comparison Pages** (expandable to 100+)
- 💙 **Beautiful Blue Gradient Design**
- 📱 **Fully Responsive** (mobile-first)
- ⚡ **Fast** (static site, <100ms load)
- 🔍 **SEO Optimized** (sitemap, meta tags, structured data)
- 🤖 **AI Generated Content** (GPT-4 via OpenRouter)
- 🔄 **Auto-Deploy** (GitHub → Cloudflare Pages)

---

## 🚀 Quick Deploy to Cloudflare Pages

### 1. Fork or Clone This Repo

```bash
git clone https://github.com/rafapra3008/cryptocompare.git
cd cryptocompare
```

### 2. Go to Cloudflare Pages

👉 **https://pages.cloudflare.com/**

1. Click **"Create a project"**
2. Connect to **GitHub**
3. Select this repository
4. Use these **build settings:**

```yaml
Build command: cd model_c_comparison/site && hugo -D
Build output directory: model_c_comparison/site/public
Root directory: (leave empty)

Environment variables:
  HUGO_VERSION = 0.152.2
```

5. Click **"Save and Deploy"**
6. ✅ **Site live in 2 minutes!**

---

## 📁 Project Structure

```
cryptocompare/
├── model_c_comparison/          # Main comparison tool
│   ├── site/                    # Hugo static site
│   │   ├── content/comparisons/ # Markdown pages (5 pages)
│   │   ├── layouts/             # Hugo templates (blue gradient)
│   │   └── public/              # Built HTML (auto-generated)
│   ├── generated/               # AI-generated content (JSON)
│   ├── preview/                 # HTML previews
│   ├── generate_content.py      # GPT-4 content generator
│   └── keywords.csv             # SEO keywords
├── shared/                      # Shared utilities
│   ├── config.py                # Configuration
│   ├── db.py                    # Database utilities
│   └── api_coingecko.py         # CoinGecko API client
├── scripts/                     # Automation scripts
│   ├── fetch_prices.py          # Hourly price updates
│   ├── health_check.py          # Monitoring
│   └── daily_jobs.sh            # Cron automation
└── docs/                        # Documentation
    ├── CLOUDFLARE_DEPLOY.md     # Deployment guide
    ├── ACCOUNTS_SETUP.md        # Affiliate setup
    └── READY.md                 # Quick start
```

---

## 🛠️ Local Development

### Prerequisites

- Hugo v0.152.2+ ([Install Hugo](https://gohugo.io/installation/))
- Python 3.11+
- Git

### Run Locally

```bash
# Navigate to Hugo site
cd model_c_comparison/site

# Start development server
hugo server -D

# Open browser
open http://localhost:1313
```

### Build for Production

```bash
cd model_c_comparison/site
hugo -D
# Built files in public/
```

---

## 🔑 Environment Setup (Optional - For Real Content)

To generate real GPT-4 content with affiliate links:

1. **Copy env template:**
   ```bash
   cp .env.example .env
   ```

2. **Add API keys:**
   ```bash
   OPENROUTER_API_KEY=sk-or-v1-xxxxx
   BINANCE_AFFILIATE_ID=xxxxx
   COINBASE_AFFILIATE_ID=xxxxx
   KRAKEN_AFFILIATE_ID=xxxxx
   ```

3. **Generate content:**
   ```bash
   cd model_c_comparison
   python3 generate_content.py
   ```

See [`ACCOUNTS_SETUP.md`](ACCOUNTS_SETUP.md) for detailed instructions.

---

## 📊 Tech Stack

- **Static Site Generator:** [Hugo](https://gohugo.io/) v0.152.2
- **Hosting:** [Cloudflare Pages](https://pages.cloudflare.com/) (Free)
- **AI Content:** GPT-4 via [OpenRouter](https://openrouter.ai/)
- **Analytics:** Cloudflare Analytics (Free)
- **Database:** PostgreSQL (optional)
- **Price Data:** [CoinGecko API](https://www.coingecko.com/en/api) (Free)

---

## 🎨 Design

- **Colors:** Blue gradient (#2563eb → #0891b2) 💙
- **Typography:** System fonts (-apple-system, BlinkMacSystemFont)
- **Responsive:** Mobile-first, works on all devices
- **Performance:** Static HTML, minimal CSS, no JavaScript

---

## 📈 Roadmap

- [x] Initial 5 comparison pages (demo content)
- [x] Blue gradient design
- [x] Hugo static site
- [x] Cloudflare Pages deployment
- [ ] Real GPT-4 content generation
- [ ] Affiliate links integration
- [ ] Google Search Console setup
- [ ] 20 comparison pages (Week 2)
- [ ] 50 pages (Month 1)
- [ ] 100+ pages (Month 3)
- [ ] Custom domain setup
- [ ] Analytics dashboard
- [ ] Automated content updates

---

## 💰 Revenue Projections

| Milestone | Timeline | Traffic | Revenue/Month |
|-----------|----------|---------|---------------|
| Launch | Week 1 | 100 | €10-20 |
| Growth | Month 1 | 500 | €50-100 |
| Scale | Month 3 | 5,000 | €500-1,000 |
| Target | Month 6 | 25,000 | €2,000-3,000 |
| **Goal** | **Month 12** | **50,000** | **€5,000+** |

Conservative estimates based on 2% click-through and 10% conversion rates.

---

## 🤝 Contributing

This is a personal revenue project, but feedback welcome!

1. Fork the repo
2. Create feature branch
3. Submit pull request

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/rafapra3008/cryptocompare/issues)
- **Docs:** See `/docs` folder for detailed guides

---

## 🎯 Current Status

**Version:** 1.0.0 (Demo)  
**Pages:** 5 comparison pages  
**Status:** ✅ Ready to deploy  
**Next:** Cloudflare Pages deployment

---

**Built with 💙 by** [rafapra3008](https://github.com/rafapra3008)

**Making the world better, one comparison at a time!** 🌍✨
