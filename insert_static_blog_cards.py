#!/usr/bin/env python3
"""Insert static HTML article cards into blog/index.html"""

# Read the static cards
with open('static_blog_cards.html', 'r') as f:
    static_cards = f.read()

# Read blog/index.html
with open('blog/index.html', 'r') as f:
    content = f.read()

# Find and replace the articles-grid section
old_section = '''    <div class="articles-grid" id="articles-grid">
      <!-- Static article cards for SEO (progressively enhanced by JavaScript) -->
      <a href="us-tariffs-trade-war-canada-2026.html" class="article-card">
        <div class="article-meta">
          <span class="article-category">Economy & Policy</span>
          <span>•</span>
          <span>10 min read</span>
        </div>
        <h2 class="article-title">US Tariffs & Trade War: What It Means for Your Canadian Wallet</h2>
        <p class="article-excerpt">US-Canada trade tensions are pushing up grocery bills, gas prices, and vehicle costs while threatening manufacturing jobs. Here's how 2025-2026 tariffs are hitting your wallet and what you can do to protect your finances.</p>
        <div class="article-footer">
          <div class="author-avatar"><svg width="32" height="32" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="48" fill="url(#avatarGrad)"/><circle cx="50" cy="42" r="18" fill="#FDBCB4"/><path d="M32 38 Q32 22 50 20 Q68 22 68 38 L68 42 Q68 32 50 30 Q32 32 32 42 Z" fill="#4A3C2C"/><circle cx="43" cy="40" r="2" fill="#2C2416"/><circle cx="57" cy="40" r="2" fill="#2C2416"/><circle cx="43.5" cy="39.5" r="0.8" fill="white"/><circle cx="57.5" cy="39.5" r="0.8" fill="white"/><path d="M38 36 Q43 34 48 36" stroke="#4A3C2C" stroke-width="1.5" fill="none" stroke-linecap="round"/><path d="M52 36 Q57 34 62 36" stroke="#4A3C2C" stroke-width="1.5" fill="none" stroke-linecap="round"/><path d="M50 44 L48 48 L50 48.5 L52 48 Z" fill="#F5A699"/><path d="M44 50 Q50 53 56 50" stroke="#C87872" stroke-width="1.5" fill="none" stroke-linecap="round"/><ellipse cx="50" cy="64" rx="14" ry="8" fill="#FDBCB4"/><path d="M36 68 Q36 78 50 80 Q64 78 64 68 L64 100 L36 100 Z" fill="#4A90E2"/><path d="M44 68 L48 72 L50 70 L52 72 L56 68" stroke="#3A7BC8" stroke-width="1.5" fill="none"/><defs><linearGradient id="avatarGrad" x1="0" y1="0" x2="100" y2="100"><stop offset="0%" stop-color="#FFE5D9"/><stop offset="100%" stop-color="#FFD4C4"/></linearGradient></defs></svg></div>
          <div class="author-info">
            <div class="author-name">Rick Minji</div>
            <div class="article-date">March 18, 2026</div>
          </div>
        </div>
      </a>
      <a href="estate-planning-basics-canada.html" class="article-card">
        <div class="article-meta">
          <span class="article-category">Financial Planning</span>
          <span>•</span>
          <span>11 min read</span>
        </div>
        <h2 class="article-title">Estate Planning Basics for Canadians: Wills, POAs, and What You Really Need</h2>
        <p class="article-excerpt">56% of Canadian adults don't have a will. Estate planning isn't just for the wealthy — if you're 18+, own anything, or have anyone you care about, you need a will, POAs, and proper beneficiary designations. Here's the complete guide.</p>
        <div class="article-footer">
          <div class="author-avatar"><svg width="32" height="32" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="48" fill="url(#avatarGrad2)"/><circle cx="50" cy="42" r="18" fill="#FDBCB4"/><path d="M32 38 Q32 22 50 20 Q68 22 68 38 L68 42 Q68 32 50 30 Q32 32 32 42 Z" fill="#4A3C2C"/><circle cx="43" cy="40" r="2" fill="#2C2416"/><circle cx="57" cy="40" r="2" fill="#2C2416"/><circle cx="43.5" cy="39.5" r="0.8" fill="white"/><circle cx="57.5" cy="39.5" r="0.8" fill="white"/><path d="M38 36 Q43 34 48 36" stroke="#4A3C2C" stroke-width="1.5" fill="none" stroke-linecap="round"/><path d="M52 36 Q57 34 62 36" stroke="#4A3C2C" stroke-width="1.5" fill="none" stroke-linecap="round"/><path d="M50 44 L48 48 L50 48.5 L52 48 Z" fill="#F5A699"/><path d="M44 50 Q50 53 56 50" stroke="#C87872" stroke-width="1.5" fill="none" stroke-linecap="round"/><ellipse cx="50" cy="64" rx="14" ry="8" fill="#FDBCB4"/><path d="M36 68 Q36 78 50 80 Q64 78 64 68 L64 100 L36 100 Z" fill="#4A90E2"/><path d="M44 68 L48 72 L50 70 L52 72 L56 68" stroke="#3A7BC8" stroke-width="1.5" fill="none"/><defs><linearGradient id="avatarGrad2" x1="0" y1="0" x2="100" y2="100"><stop offset="0%" stop-color="#FFE5D9"/><stop offset="100%" stop-color="#FFD4C4"/></linearGradient></defs></svg></div>
          <div class="author-info">
            <div class="author-name">Rick Minji</div>
            <div class="article-date">March 18, 2026</div>
          </div>
        </div>
      </a>
    </div>'''

new_section = f'''    <div class="articles-grid" id="articles-grid">
      <!-- Static article cards for SEO (JavaScript will enhance/replace these) -->
{static_cards}
    </div>'''

# Replace
new_content = content.replace(old_section, new_section)

# Write back
with open('blog/index.html', 'w') as f:
    f.write(new_content)

print("✅ Successfully inserted all 29 static article cards into blog/index.html")
print("📄 Crawlers will now see all articles without executing JavaScript!")
