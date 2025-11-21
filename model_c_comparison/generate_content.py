"""
Content Generator for Model C (CryptoCompare)
Generates comparison pages using GPT-4
"""
import os
import json
import logging
from datetime import datetime
from typing import Dict, List
import requests

logger = logging.getLogger(__name__)

class ComparisonPageGenerator:
    def __init__(self, api_key: str):
        """
        Initialize with OpenRouter API key (for GPT-4 access)
        OpenRouter is cheaper than direct OpenAI
        """
        self.api_key = api_key
        self.model = "openai/gpt-4-turbo"
        self.base_url = "https://openrouter.ai/api/v1"
    
    def generate_comparison_page(self, keyword: str, exchanges: List[str]) -> Dict:
        """
        Generate a complete comparison page
        
        Args:
            keyword: Target SEO keyword (e.g., "best crypto exchange italy 2025")
            exchanges: List of exchanges to compare (e.g., ["Binance", "Coinbase"])
        
        Returns:
            Dict with {title, meta_description, html_content}
        """
        
        prompt = self._build_prompt(keyword, exchanges)
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an expert crypto content writer specializing in SEO-optimized comparison articles."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.3,  # Lower = more factual
                    "max_tokens": 3000
                },
                timeout=60
            )
            
            response.raise_for_status()
            data = response.json()
            
            content_json = data['choices'][0]['message']['content']
            
            # Parse JSON response
            # Sometimes GPT wraps in markdown code blocks
            if '```json' in content_json:
                content_json = content_json.split('```json')[1].split('```')[0].strip()
            elif '```' in content_json:
                content_json = content_json.split('```')[1].split('```')[0].strip()
            
            result = json.loads(content_json)
            
            # Add metadata
            result['generated_at'] = datetime.now().isoformat()
            result['keyword'] = keyword
            result['model_used'] = self.model
            
            logger.info(f"Generated page for keyword: {keyword}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating page: {e}")
            # Return fallback template
            return self._fallback_template(keyword, exchanges)
    
    def _build_prompt(self, keyword: str, exchanges: List[str]) -> str:
        """Build the GPT prompt"""
        
        exchanges_str = ", ".join(exchanges)
        
        prompt = f"""
Generate a comprehensive SEO-optimized comparison page for the keyword: "{keyword}"

Exchanges to compare: {exchanges_str}

**Requirements:**

1. **Structure:**
   - H1: Use the exact keyword "{keyword}" (include year 2025)
   - Quick Answer section (2-3 sentences, direct answer)
   - Comparison Table (Exchange | Fees | Coins | Rating | CTA Button)
   - Detailed review of each exchange (200-300 words per exchange)
     - Pros (3-5 bullet points)
     - Cons (2-3 bullet points)
     - Best for (who should use it)
   - "How to Choose" guide (5-7 factors to consider)
   - FAQ section (5 questions and answers)
   - Disclaimer section (affiliate + not financial advice)

2. **SEO:**
   - Use keyword "{keyword}" 3-5 times naturally (1-2% density)
   - Include related long-tail keywords
   - Meta description: <160 characters, include keyword + year
   - Headers: Use H2 for main sections, H3 for subsections

3. **Tone:**
   - Professional but accessible (Flesch Reading Ease: 60+)
   - Data-driven (use specific numbers for fees, coins, etc.)
   - Honest (don't be overly promotional)

4. **Data (use realistic estimates):**
   - Binance: 0.1% trading fee, 350+ coins, 4.5/5 rating
   - Coinbase: 1.49% trading fee, 200+ coins, 4.3/5 rating
   - Kraken: 0.16% trading fee, 150+ coins, 4.4/5 rating
   - Crypto.com: 0.4% trading fee, 250+ coins, 4.2/5 rating
   (Adjust as needed for other exchanges)

5. **Compliance:**
   - Affiliate disclosure:  "⚠️ This page contains affiliate links. We may earn a commission if you sign up, at no extra cost to you."
   - Financial disclaimer: "📋 Disclaimer: This information is for educational purposes only and does not constitute financial advice."
   - Last updated date

6. **CTA Buttons (use placeholder text):**
   - "Get €100 Bonus" (for Binance)
   - "Get €10 Free" (for Coinbase)
   - "Start Trading" (generic)

**Output Format (STRICT JSON):**
{{
  "title": "...",
  "meta_description": "...",
  "html_content": "... (full HTML with proper tags: <h2>, <h3>, <table>, <ul>, <p>, etc.)"
}}

**IMPORTANT:**
- Output ONLY valid JSON
- Escape quotes in HTML content properly
- Include complete HTML (not markdown)
- Make it pass Google's E-E-A-T guidelines
"""
        
        return prompt
    
    def _fallback_template(self, keyword: str, exchanges: List[str]) -> Dict:
        """Fallback template if GPT fails"""
        exchanges_list = "</li><li>".join(exchanges)
        
        return {
            "title": keyword.title(),
            "meta_description": f"{keyword} - Compare fees, features, and ratings. Updated 2025.",
            "html_content": f"""
<article>
    <h1>{keyword.title()}</h1>
    
    <div class="quick-answer">
        <p><strong>Quick Answer:</strong> We're comparing: {", ".join(exchanges)}.</p>
    </div>
    
    <h2>Exchanges Compared</h2>
    <ul>
        <li>{exchanges_list}</li>
    </ul>
    
    <p class="disclaimer">⚠️ This page contains affiliate links.</p>
    <p class="disclaimer">📋 Not financial advice.</p>
</article>
            """,
            "generated_at": datetime.now().isoformat(),
            "keyword": keyword,
            "fallback": True
        }
    
    def batch_generate(self, keywords_list: List[Dict]) -> List[Dict]:
        """
        Generate multiple pages in batch
        
        Args:
            keywords_list: List of {keyword: str, exchanges: List[str]}
        
        Returns:
            List of generated pages
        """
        results = []
        
        for i, item in enumerate(keywords_list):
            logger.info(f"Generating {i+1}/{len(keywords_list)}: {item['keyword']}")
            
            page = self.generate_comparison_page(
                keyword=item['keyword'],
                exchanges=item['exchanges']
            )
            
            results.append(page)
            
            # Rate limiting (OpenRouter has limits)
            if i < len(keywords_list) - 1:
                import time
                time.sleep(2)  # 2 seconds between requests
        
        return results

if __name__ == "__main__":
    # Test
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from shared.config import Config
    
    generator = ComparisonPageGenerator(Config.OPENROUTER_API_KEY)
    
    test_keywords = [
        {
            "keyword": "best crypto exchange italy 2025",
            "exchanges": ["Binance", "Coinbase", "Kraken"]
        }
    ]
    
    pages = generator.batch_generate(test_keywords)
    
    # Save to file
    for page in pages:
        filename = page['keyword'].replace(' ', '_') + '.json'
        with open(f"output/{filename}", 'w') as f:
            json.dump(page, f, indent=2)
        
        print(f"✅ Generated: {page['title']}")
