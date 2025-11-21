#!/usr/bin/env python3
"""
Quick demo: Generate ONE test page and show it
No API key needed for demo mode
"""
import json
from pathlib import Path

# Demo template (no GPT-4 needed)
def generate_demo_page():
    """Generate a demo comparison page without AI"""
    
    demo_page = {
        "title": "Best Crypto Exchange Italy 2025 - Complete Guide",
        "meta_description": "Compare top crypto exchanges for Italy in 2025. Binance, Coinbase, Kraken - fees, features, and security compared. Updated Nov 2025.",
        "keyword": "best crypto exchange italy 2025",
        "html_content": """
<article class="comparison-page">
    <div class="hero">
        <h1>Best Crypto Exchange Italy 2025 - Complete Comparison</h1>
        <p class="lead">Finding the best crypto exchange in Italy? We've compared the top platforms so you don't have to.</p>
        <p class="updated">Last Updated: November 22, 2025</p>
    </div>

    <div class="quick-answer">
        <h2>🎯 Quick Answer</h2>
        <p><strong>TL;DR:</strong> The best crypto exchange for Italy is <strong>Binance</strong> for advanced traders (lowest fees at 0.1%) and <strong>Coinbase</strong> for beginners (easiest interface). Kraken offers the best balance of fees and security.</p>
    </div>

    <section class="comparison-table">
        <h2>📊 Top 3 Crypto Exchanges Compared</h2>
        <table>
            <thead>
                <tr>
                    <th>Exchange</th>
                    <th>Trading Fees</th>
                    <th>Coins</th>
                    <th>Rating</th>
                    <th>Best For</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>🥇 Binance</strong></td>
                    <td>0.1%</td>
                    <td>350+</td>
                    <td>⭐⭐⭐⭐⭐ 4.5/5</td>
                    <td>Advanced traders</td>
                    <td><a href="#binance" class="btn btn-primary">Get €100 Bonus</a></td>
                </tr>
                <tr>
                    <td><strong>🥈 Coinbase</strong></td>
                    <td>1.49%</td>
                    <td>200+</td>
                    <td>⭐⭐⭐⭐ 4.3/5</td>
                    <td>Beginners</td>
                    <td><a href="#coinbase" class="btn btn-secondary">Get €10 Free</a></td>
                </tr>
                <tr>
                    <td><strong>🥉 Kraken</strong></td>
                    <td>0.16%</td>
                    <td>150+</td>
                    <td>⭐⭐⭐⭐ 4.4/5</td>
                    <td>Security-focused</td>
                    <td><a href="#kraken" class="btn btn-secondary">Start Trading</a></td>
                </tr>
            </tbody>
        </table>
    </section>

    <section class="detailed-reviews">
        <h2>🔍 Detailed Exchange Reviews</h2>

        <article id="binance" class="exchange-review">
            <h3>1. Binance - Best for Advanced Traders</h3>
            
            <div class="pros-cons">
                <div class="pros">
                    <h4>✅ Pros</h4>
                    <ul>
                        <li>Lowest trading fees (0.1%)</li>
                        <li>350+ cryptocurrencies available</li>
                        <li>Advanced trading tools (futures, margin, spot)</li>
                        <li>High liquidity for all major pairs</li>
                        <li>Staking and earning options</li>
                    </ul>
                </div>
                <div class="cons">
                    <h4>❌ Cons</h4>
                    <ul>
                        <li>Complex interface for beginners</li>
                        <li>Customer support can be slow</li>
                        <li>Requires KYC verification (up to 7 days)</li>
                    </ul>
                </div>
            </div>

            <p><strong>Best For:</strong> Day traders, high-volume users, and experienced crypto investors who need advanced features and low fees.</p>

            <p><strong>Italy-Specific:</strong> Binance supports SEPA transfers for EUR deposits, making it easy for Italian users to fund accounts.</p>

            <a href="#" class="cta-button">Sign Up to Binance →</a>
        </article>

        <article id="coinbase" class="exchange-review">
            <h3>2. Coinbase - Best for Beginners</h3>
            
            <div class="pros-cons">
                <div class="pros">
                    <h4>✅ Pros</h4>
                    <ul>
                        <li>Extremely user-friendly interface</li>
                        <li>Excellent mobile app</li>
                        <li>Strong security (insurance for USD balances)</li>
                        <li>Educational resources (Coinbase Earn)</li>
                        <li>Publicly traded company (COIN on NASDAQ)</li>
                    </ul>
                </div>
                <div class="cons">
                    <h4>❌ Cons</h4>
                    <ul>
                        <li>Higher fees (1.49% for card purchases)</li>
                        <li>Fewer cryptocurrencies than Binance</li>
                        <li>Limited advanced trading features</li>
                    </ul>
                </div>
            </div>

            <p><strong>Best For:</strong> Complete beginners, investors who prioritize simplicity and security over low fees.</p>

            <p><strong>Italy-Specific:</strong> Coinbase is fully registered in Italy and complies with EU MiCA regulations.</p>

            <a href="#" class="cta-button">Sign Up to Coinbase →</a>
        </article>

        <article id="kraken" class="exchange-review">
            <h3>3. Kraken - Best for Security</h3>
            
            <div class="pros-cons">
                <div class="pros">
                    <h4>✅ Pros</h4>
                    <ul>
                        <li>Never been hacked (industry-leading security)</li>
                        <li>Low fees (0.16% average)</li>
                        <li>Excellent customer support</li>
                        <li>Staking rewards available</li>
                        <li>Transparent fee structure</li>
                    </ul>
                </div>
                <div class="cons">
                    <h4>❌ Cons</h4>
                    <ul>
                        <li>Fewer coins than Binance (150 vs 350)</li>
                        <li>Interface can feel dated</li>
                        <li>Higher withdrawal fees</li>
                    </ul>
                </div>
            </div>

            <p><strong>Best For:</strong> Security-conscious investors who want a trusted platform with good fees.</p>

            <p><strong>Italy-Specific:</strong> Kraken has been operating in Europe since 2011 and is fully compliant with Italian/EU regulations.</p>

            <a href="#" class="cta-button">Sign Up to Kraken →</a>
        </article>
    </section>

    <section class="how-to-choose">
        <h2>🎓 How to Choose the Right Crypto Exchange</h2>
        
        <p>When selecting a crypto exchange in Italy, consider these key factors:</p>

        <ol>
            <li><strong>Fees:</strong> Trading fees range from 0.1% (Binance) to 1.49% (Coinbase). If you're planning to trade frequently, lower fees save hundreds of euros per year.</li>
            
            <li><strong>Security:</strong> Look for 2FA (two-factor authentication), cold storage, and insurance. Kraken and Coinbase have the best security track records.</li>
            
            <li><strong>Number of Coins:</strong> If you want access to new altcoins, Binance (350+ coins) is better than Kraken (150 coins).</li>
            
            <li><strong>Ease of Use:</strong> Beginners should prioritize user-friendly interfaces. Coinbase wins here.</li>
            
            <li><strong>Regulation:</strong> All three exchanges are legal in Italy, but Coinbase and Kraken are more transparent about compliance.</li>

            <li><strong>Payment Methods:</strong> Check if the exchange supports SEPA transfers (all three do) for easy EUR deposits.</li>

            <li><strong>Customer Support:</strong> Kraken has the best support. Binance can be slow during high-volume periods.</li>
        </ol>
    </section>

    <section class="faq">
        <h2>❓ Frequently Asked Questions</h2>

        <div class="faq-item">
            <h3>Are crypto exchanges legal in Italy?</h3>
            <p>Yes, cryptocurrency exchanges are legal in Italy. However, they must comply with EU regulations (including the upcoming MiCA framework). All three exchanges listed here are compliant.</p>
        </div>

        <div class="faq-item">
            <h3>Which exchange has the lowest fees?</h3>
            <p>Binance has the lowest trading fees at 0.1% per trade. Kraken is second at 0.16%, while Coinbase charges 1.49% for standard purchases.</p>
        </div>

        <div class="faq-item">
            <h3>Do I need to pay taxes on crypto in Italy?</h3>
            <p>Yes. In Italy, cryptocurrency gains above €2,000 per year are taxable at 26%. You must declare crypto holdings on your tax return (Quadro RW).</p>
        </div>

        <div class="faq-item">
            <h3>How long does verification take?</h3>
            <p>KYC verification typically takes 1-7 days. Coinbase is usually fastest (24-48 hours), Binance can take up to a week during busy periods.</p>
        </div>

        <div class="faq-item">
            <h3>Can I use EUR on these exchanges?</h3>
            <p>Yes, all three exchanges support EUR deposits via SEPA bank transfer. Binance and Coinbase also accept credit/debit cards (with higher fees).</p>
        </div>
    </section>

    <section class="disclaimer">
        <h2>⚠️ Important Disclaimers</h2>
        
        <div class="disclaimer-box">
            <p><strong>Affiliate Disclosure:</strong> This page contains affiliate links to crypto exchanges. If you sign up through our links, we may earn a commission at no extra cost to you. This helps us maintain this free resource.</p>
            
            <p><strong>Not Financial Advice:</strong> The information on this page is for educational purposes only and does not constitute financial advice. Cryptocurrency investments are risky and volatile. Always do your own research and invest only what you can afford to lose.</p>
            
            <p><strong>Risk Warning:</strong> Cryptocurrencies are highly volatile. Prices can fluctuate significantly in short periods. Past performance does not guarantee future results.</p>
        </div>
    </section>

    <footer>
        <p><em>Last updated: November 22, 2025</em></p>
        <p><em>Information accuracy: We strive to keep this comparison up-to-date, but fees and features may change. Always check the exchange's official website for current information.</em></p>
    </footer>
</article>
""",
        "generated_at": "2025-11-22T00:00:00Z",
        "model_used": "demo-template",
        "fallback": False
    }
    
    return demo_page

def main():
    print("🎨 Generating DEMO comparison page (no AI needed)...")
    print("=" * 60)
    
    # Generate demo page
    page = generate_demo_page()
    
    # Create output directory
    output_dir = Path(__file__).parent / "generated"
    output_dir.mkdir(exist_ok=True)
    
    # Save JSON
    output_file = output_dir / f"{page['keyword'].replace(' ', '_')}.json"
    with open(output_file, 'w') as f:
        json.dump(page, f, indent=2)
    
    print(f"✅ Demo page generated!")
    print(f"📄 File: {output_file}")
    print(f"📊 Title: {page['title']}")
    print(f"📝 Word count: ~{len(page['html_content'].split())} words")
    print()
    print("Next step:")
    print("  python3 build_site.py")
    print()
    print("Or with real AI:")
    print("  1. Get OpenRouter API key: https://openrouter.ai/")
    print("  2. Add to .env: OPENROUTER_API_KEY=sk-...")
    print("  3. Run: python3 generate_content.py")

if __name__ == "__main__":
    main()
