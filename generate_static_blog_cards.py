#!/usr/bin/env python3
"""Generate static HTML article cards for blog/index.html"""

import json
from datetime import datetime

# Read articles.json
with open('blog/articles.json', 'r') as f:
    articles = json.load(f)

# Rick Minji avatar SVG (inline)
avatar_svg = """<svg width="32" height="32" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="50" cy="50" r="48" fill="url(#avatarGrad)"/>
      <circle cx="50" cy="42" r="18" fill="#FDBCB4"/>
      <path d="M32 38 Q32 22 50 20 Q68 22 68 38 L68 42 Q68 32 50 30 Q32 32 32 42 Z" fill="#4A3C2C"/>
      <circle cx="43" cy="40" r="2" fill="#2C2416"/>
      <circle cx="57" cy="40" r="2" fill="#2C2416"/>
      <circle cx="43.5" cy="39.5" r="0.8" fill="white"/>
      <circle cx="57.5" cy="39.5" r="0.8" fill="white"/>
      <path d="M38 36 Q43 34 48 36" stroke="#4A3C2C" stroke-width="1.5" fill="none" stroke-linecap="round"/>
      <path d="M52 36 Q57 34 62 36" stroke="#4A3C2C" stroke-width="1.5" fill="none" stroke-linecap="round"/>
      <path d="M50 44 L48 48 L50 48.5 L52 48 Z" fill="#F5A699"/>
      <path d="M44 50 Q50 53 56 50" stroke="#C87872" stroke-width="1.5" fill="none" stroke-linecap="round"/>
      <ellipse cx="50" cy="64" rx="14" ry="8" fill="#FDBCB4"/>
      <path d="M36 68 Q36 78 50 80 Q64 78 64 68 L64 100 L36 100 Z" fill="#4A90E2"/>
      <path d="M44 68 L48 72 L50 70 L52 72 L56 68" stroke="#3A7BC8" stroke-width="1.5" fill="none"/>
      <defs>
        <linearGradient id="avatarGrad" x1="0" y1="0" x2="100" y2="100">
          <stop offset="0%" stop-color="#FFE5D9"/>
          <stop offset="100%" stop-color="#FFD4C4"/>
        </linearGradient>
      </defs>
    </svg>"""

def format_date(date_str):
    """Format date like 'February 10, 2026'"""
    date = datetime.strptime(date_str, '%Y-%m-%d')
    return date.strftime('%B %d, %Y')

# Generate static HTML cards
html_cards = []
for article in articles:
    card_html = f"""      <a href="{article['slug']}.html" class="article-card">
        <div class="article-meta">
          <span class="article-category">{article['category']}</span>
          <span>•</span>
          <span>{article['readTime']}</span>
        </div>
        <h2 class="article-title">{article['title']}</h2>
        <p class="article-excerpt">{article['excerpt']}</p>
        <div class="article-footer">
          <div class="author-avatar">{avatar_svg}</div>
          <div class="author-info">
            <div class="author-name">{article['author']}</div>
            <div class="article-date">{format_date(article['date'])}</div>
          </div>
        </div>
      </a>"""
    html_cards.append(card_html)

# Join all cards
static_cards_html = '\n'.join(html_cards)

# Write to file for inspection
with open('static_blog_cards.html', 'w') as f:
    f.write(static_cards_html)

print(f"✅ Generated {len(html_cards)} static article cards")
print(f"📄 Saved to static_blog_cards.html")
print(f"\nNow updating blog/index.html...")
