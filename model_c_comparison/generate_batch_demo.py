#!/usr/bin/env python3
"""
Generate 5 demo comparison pages (no API key needed)
Different keywords for variety
"""
import json
from pathlib import Path
from datetime import datetime

def generate_pages():
    """Generate 5 different comparison pages"""
    
    pages_config = [
        {
            "keyword": "best crypto exchange italy 2025",
            "exchanges": ["Binance", "Coinbase", "Kraken"],
            "focus": "Italy-specific features"
        },
        {
            "keyword": "binance vs coinbase",
            "exchanges": ["Binance", "Coinbase"],
            "focus": "Head-to-head comparison"
        },
        {
            "keyword": "cheapest crypto exchange fees",
            "exchanges": ["Binance", "Kraken", "Bitstamp"],
            "focus": "Fee comparison"
        },
        {
            "keyword": "best crypto exchange for beginners",
            "exchanges": ["Coinbase", "Crypto.com", "Binance"],
            "focus": "Ease of use"
        },
        {
            "keyword": "best exchange for bitcoin",
            "exchanges": ["Binance", "Coinbase", "Kraken"],
            "focus": "Bitcoin trading features"
        }
    ]
    
    output_dir = Path(__file__).parent / "generated"
    output_dir.mkdir(exist_ok=True)
    
    pages_generated = []
    
    for config in pages_config:
        # Create simplified page structure
        page = {
            "title": f"{config['keyword'].title()} - Complete Guide",
            "meta_description": f"Compare {', '.join(config['exchanges'])} in 2025. Fees, features, security. Updated Nov 2025.",
            "keyword": config['keyword'],
            "html_content": generate_html_content(config),
            "generated_at": datetime.now().isoformat(),
            "model_used": "demo-batch-template",
            "fallback": False
        }
        
        # Save JSON
        filename = config['keyword'].replace(' ', '_') + '.json'
        filepath = output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(page, f, indent=2)
        
        print(f"✅ Generated: {config['keyword']}")
        pages_generated.append(filepath)
    
    return pages_generated

def generate_html_content(config):
    """Generate HTML content for a comparison page"""
    
    exchanges_rows = ""
    for i, exchange in enumerate(config['exchanges']):
        medal = ["🥇", "🥈", "🥉"][i] if i < 3 else "📊"
        fees = {
            "Binance": "0.1%",
            "Coinbase": "1.49%",
            "Kraken": "0.16%",
            "Crypto.com": "0.4%",
            "Bitstamp": "0.5%"
        }.get(exchange, "0.2%")
        
        coins = {
            "Binance": "350+",
            "Coinbase": "200+",
            "Kraken": "150+",
            "Crypto.com": "250+",
            "Bitstamp": "80+"
        }.get(exchange, "100+")
        
        rating = {
            "Binance": "4.5/5",
            "Coinbase": "4.3/5",
            "Kraken": "4.4/5",
            "Crypto.com": "4.2/5",
            "Bitstamp": "4.0/5"
        }.get(exchange, "4.0/5")
        
        exchanges_rows += f"""
                <tr>
                    <td><strong>{medal} {exchange}</strong></td>
                    <td>{fees}</td>
                    <td>{coins}</td>
                    <td>⭐ {rating}</td>
                    <td><a href="#{exchange.lower()}" class="btn">Sign Up →</a></td>
                </tr>"""
    
    html = f"""
<article class="comparison-page">
    <h1>{config['keyword'].title()}</h1>
    
    <div class="quick-answer">
        <h2>🎯 Quick Answer</h2>
        <p><strong>TL;DR:</strong> Comparing {', '.join(config['exchanges'])} based on {config['focus']}.</p>
    </div>

    <section class="comparison-table">
        <h2>📊 Comparison Table</h2>
        <table>
            <thead>
                <tr>
                    <th>Exchange</th>
                    <th>Fees</th>
                    <th>Coins</th>
                    <th>Rating</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>{exchanges_rows}
            </tbody>
        </table>
    </section>

    <section class="faq">
        <h2>❓ FAQ</h2>
        <div class="faq-item">
            <h3>Which is the best overall?</h3>
            <p>It depends on your needs. {config['exchanges'][0]} is great for {config['focus']}.</p>
        </div>
    </section>

    <section class="disclaimer">
        <h2>⚠️ Disclaimers</h2>
        <p><strong>Affiliate Disclosure:</strong> This page contains affiliate links.</p>
        <p><strong>Not Financial Advice:</strong> For educational purposes only.</p>
    </section>

    <footer>
        <p><em>Last updated: November 21, 2025</em></p>
    </footer>
</article>
"""
    
    return html

if __name__ == "__main__":
    print("🎨 Generating 5 demo comparison pages...")
    print("=" * 60)
    
    pages = generate_pages()
    
    print("=" * 60)
    print(f"✅ Generated {len(pages)} pages")
    print()
    print("Next step:")
    print("  python3 build_site.py")
    print()
    print("Files created:")
    for page in pages:
        print(f"  📄 {page.name}")
