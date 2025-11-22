#!/usr/bin/env python3
import os
from datetime import datetime

# Top 20 price pages configuration
# Slug, Title, Coin Symbol, Currency
pages = [
    ("bitcoin-usd", "Bitcoin Price USD", "BTC", "USD"),
    ("bitcoin-eur", "Bitcoin Price EUR", "BTC", "EUR"),
    ("ethereum-usd", "Ethereum Price USD", "ETH", "USD"),
    ("ethereum-eur", "Ethereum Price EUR", "ETH", "EUR"),
    ("bitcoin-gbp", "Bitcoin Price GBP", "BTC", "GBP"),
    ("ethereum-gbp", "Ethereum Price GBP", "ETH", "GBP"),
    ("solana-usd", "Solana Price USD", "SOL", "USD"),
    ("binancecoin-usd", "BNB Price USD", "BNB", "USD"),
    ("ripple-usd", "XRP Price USD", "XRP", "USD"),
    ("cardano-usd", "Cardano Price USD", "ADA", "USD"),
    ("avalanche-usd", "Avalanche Price USD", "AVAX", "USD"),
    ("dogecoin-usd", "Dogecoin Price USD", "DOGE", "USD"),
    ("polkadot-usd", "Polkadot Price USD", "DOT", "USD"),
    ("polygon-usd", "Polygon Price USD", "MATIC", "USD"),
    ("chainlink-usd", "Chainlink Price USD", "LINK", "USD"),
    ("litecoin-usd", "Litecoin Price USD", "LTC", "USD"),
    ("shiba-inu-usd", "Shiba Inu Price USD", "SHIB", "USD"),
    ("bitcoin-cash-usd", "Bitcoin Cash Price USD", "BCH", "USD"),
    ("uniswap-usd", "Uniswap Price USD", "UNI", "USD"),
    ("stellar-usd", "Stellar Price USD", "XLM", "USD"),
]

# Ensure output directory exists
output_dir = "site/content/prices"
os.makedirs(output_dir, exist_ok=True)

print(f"🚀 Generating {len(pages)} price pages in {output_dir}...")

for slug, title, coin, currency in pages:
    # Current time for "last updated" (static for now, dynamic in JS)
    now_iso = datetime.now().isoformat()
    
    content = f'''---
title: "{title} - Live Chart & Price Today"
description: "Real-time {coin}/{currency} price, 24h chart, historical data and market analysis. Updated every minute."
date: {now_iso}
keywords: ["{coin} price", "{coin} {currency}", "{coin} live price", "buy {coin}"]
draft: false
---

<p class="lead">
    The live price of <strong>{title}</strong> is tracking at a real-time value. 
    Use our interactive chart to analyze trends and historical data.
</p>

<h2>About {coin}</h2>
<p>
    {coin} is one of the leading cryptocurrencies by market capitalization. 
    Tracking the {coin}/{currency} pair is essential for traders and investors looking to time their market entries.
</p>

<h3>Where to Buy {coin} with Low Fees?</h3>
<p>
    Don't overpay on trading fees. We recommend checking our comparison of top exchanges:
</p>

<ul>
    <li><strong>Binance:</strong> Best for low fees (0.1%) and high liquidity.</li>
    <li><strong>Kraken:</strong> Excellent for EUR/USD pairs and security.</li>
    <li><strong>Coinbase:</strong> Easiest for beginners to buy {coin} instantly.</li>
</ul>

<p>
    <a href="https://www.cryptoverso2025.com/comparisons/best-crypto-exchange-italy-2025/" class="btn">Compare All Exchanges →</a>
</p>

<h2>Live {coin} Price Analysis</h2>
<p>
    Our real-time data feed updates the {coin} price in {currency} every minute. 
    (Chart loading...)
</p>
'''
    
    file_path = os.path.join(output_dir, f"{slug}.md")
    with open(file_path, "w") as f:
        f.write(content)
    
    print(f"✅ Created: {slug}.md")

print(f"\n✨ Success! {len(pages)} pages generated.")
