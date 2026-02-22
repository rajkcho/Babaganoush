#!/usr/bin/env python3
"""Batch update remaining affiliate sections"""
import re

# Read the file
with open('index.html', 'r') as f:
    content = f.read()

# Define replacement sections
REPLACEMENTS = {
    'incometax': '''      <div class="affiliate-resources">
        <h3>📚 Recommended Resources</h3>
        <div class="affiliate-grid">
          <a href="https://www.amazon.ca/dp/0143190008?tag=figgy0a0-20" target="_blank" rel="noopener noreferrer sponsored" class="affiliate-card">
            <div class="affiliate-info">
              <span class="affiliate-title">The Wealthy Barber Returns</span>
              <span class="affiliate-author">David Chilton</span>
              <span class="affiliate-why">Tax-smart wealth building for Canadians</span>
            </div>
          </a>
          <a href="https://www.amazon.ca/dp/1459721646?tag=figgy0a0-20" target="_blank" rel="noopener noreferrer sponsored" class="affiliate-card">
            <div class="affiliate-info">
              <span class="affiliate-title">Tax-Free Savings Accounts</span>
              <span class="affiliate-author">Gordon Pape</span>
              <span class="affiliate-why">Maximize tax-free growth opportunities</span>
            </div>
          </a>
          <a href="https://www.amazon.ca/dp/0143191292?tag=figgy0a0-20" target="_blank" rel="noopener noreferrer sponsored" class="affiliate-card">
            <div class="affiliate-info">
              <span class="affiliate-title">How NOT to Move Back in with Your Parents</span>
              <span class="affiliate-author">Rob Chicken</span>
              <span class="affiliate-why">Young professional tax strategies</span>
            </div>
          </a>
          <a href="https://www.amazon.ca/dp/1523505745?tag=figgy0a0-20" target="_blank" rel="noopener noreferrer sponsored" class="affiliate-card">
            <div class="affiliate-info">
              <span class="affiliate-title">I Will Teach You to Be Rich</span>
              <span class="affiliate-author">Ramit Sethi</span>
              <span class="affiliate-why">Tax-efficient automation and investing</span>
            </div>
          </a>
          <a href="https://www.amazon.ca/dp/0857197681?tag=figgy0a0-20" target="_blank" rel="noopener noreferrer sponsored" class="affiliate-card">
            <div class="affiliate-info">
              <span class="affiliate-title">The Psychology of Money</span>
              <span class="affiliate-author">Morgan Housel</span>
              <span class="affiliate-why">Smart money decisions and tax planning</span>
            </div>
          </a>
        </div>
        <p class="affiliate-disclosure">As an Amazon Associate, FiggyBank earns from qualifying purchases.</p>
      </div>''',
    
    'salary': '''      <div class="affiliate-resources">
        <h3>📚 Recommended Resources</h3>
        <div class="affiliate-grid">
          <a href="https://www.amazon.ca/dp/0062407805?tag=figgy0a0-20" target="_blank" rel="noopener noreferrer sponsored" class="affiliate-card">
            <div class="affiliate-info">
              <span class="affiliate-title">Never Split the Difference</span>
              <span class="affiliate-author">Chris Voss</span>
              <span class="affiliate-why">Master salary negotiation tactics</span>
            </div>
          </a>
          <a href="https://www.amazon.ca/dp/0143190008?tag=figgy0a0-20" target="_blank" rel="noopener noreferrer sponsored" class="affiliate-card">
            <div class="affiliate-info">
              <span class="affiliate-title">The Wealthy Barber Returns</span>
              <span class="affiliate-author">David Chilton</span>
              <span class="affiliate-why">Make the most of your income</span>
            </div>
          </a>
          <a href="https://www.amazon.ca/dp/0143191292?tag=figgy0a0-20" target="_blank" rel="noopener noreferrer sponsored" class="affiliate-card">
            <div class="affiliate-info">
              <span class="affiliate-title">How NOT to Move Back in with Your Parents</span>
              <span class="affiliate-author">Rob Chicken</span>
              <span class="affiliate-why">Young professional compensation guide</span>
            </div>
          </a>
          <a href="https://www.amazon.ca/dp/1523505745?tag=figgy0a0-20" target="_blank" rel="noopener noreferrer sponsored" class="affiliate-card">
            <div class="affiliate-info">
              <span class="affiliate-title">I Will Teach You to Be Rich</span>
              <span class="affiliate-author">Ramit Sethi</span>
              <span class="affiliate-why">Optimize and automate your salary</span>
            </div>
          </a>
          <a href="https://www.amazon.ca/dp/0857197681?tag=figgy0a0-20" target="_blank" rel="noopener noreferrer sponsored" class="affiliate-card">
            <div class="affiliate-info">
              <span class="affiliate-title">The Psychology of Money</span>
              <span class="affiliate-author">Morgan Housel</span>
              <span class="affiliate-why">Career and compensation mindset</span>
            </div>
          </a>
        </div>
        <p class="affiliate-disclosure">As an Amazon Associate, FiggyBank earns from qualifying purchases.</p>
      </div>''',
    
    'tfsa': '''      <div class="affiliate-resources">
        <h3>📚 Recommended Resources</h3>
        <div class="affiliate-grid">
          <a href="https://www.amazon.ca/dp/1459721646?tag=figgy0a0-20" target="_blank" rel="noopener noreferrer sponsored" class="affiliate-card">
            <div class="affiliate-info">
              <span class="affiliate-title">Tax-Free Savings Accounts</span>
              <span class="affiliate-author">Gordon Pape</span>
              <span class="affiliate-why">The complete guide to TFSAs</span>
            </div>
          </a>
          <a href="https://www.amazon.ca/dp/0143190008?tag=figgy0a0-20" target="_blank" rel="noopener noreferrer sponsored" class="affiliate-card">
            <div class="affiliate-info">
              <span class="affiliate-title">The Wealthy Barber Returns</span>
              <span class="affiliate-author">David Chilton</span>
              <span class="affiliate-why">Canadian tax-free investing strategies</span>
            </div>
          </a>
          <a href="https://www.amazon.ca/dp/0143191292?tag=figgy0a0-20" target="_blank" rel="noopener noreferrer sponsored" class="affiliate-card">
            <div class="affiliate-info">
              <span class="affiliate-title">How NOT to Move Back in with Your Parents</span>
              <span class="affiliate-author">Rob Chicken</span>
              <span class="affiliate-why">TFSA strategies for young Canadians</span>
            </div>
          </a>
          <a href="https://www.amazon.ca/dp/1523505745?tag=figgy0a0-20" target="_blank" rel="noopener noreferrer sponsored" class="affiliate-card">
            <div class="affiliate-info">
              <span class="affiliate-title">I Will Teach You to Be Rich</span>
              <span class="affiliate-author">Ramit Sethi</span>
              <span class="affiliate-why">Automate your TFSA contributions</span>
            </div>
          </a>
          <a href="https://www.amazon.ca/dp/1119404509?tag=figgy0a0-20" target="_blank" rel="noopener noreferrer sponsored" class="affiliate-card">
            <div class="affiliate-info">
              <span class="affiliate-title">The Little Book of Common Sense Investing</span>
              <span class="affiliate-author">John C. Bogle</span>
              <span class="affiliate-why">Simple index investing in your TFSA</span>
            </div>
          </a>
        </div>
        <p class="affiliate-disclosure">As an Amazon Associate, FiggyBank earns from qualifying purchases.</p>
      </div>''',
}

def find_and_replace_affiliate_section(content, page_id, new_section):
    """Find affiliate section for a page and replace it"""
    # Pattern to match the affiliate-resources section for a specific page
    page_pattern = rf'(<div class="page" id="page-{page_id}".*?)'
    next_page_pattern = r'(<div class="page" id="page-[^"]+"|$)'
    
    # Find the page section
    page_match = re.search(page_pattern, content, re.DOTALL)
    if not page_match:
        print(f"  WARNING: Could not find page-{page_id}")
        return content
    
    page_start = page_match.start()
    
    # Find the next page or end of file
    next_page_match = re.search(next_page_pattern, content[page_start + 100:], re.DOTALL)
    if next_page_match:
        page_end = page_start + 100 + next_page_match.start()
    else:
        page_end = len(content)
    
    page_content = content[page_start:page_end]
    
    # Find and replace the affiliate-resources section within this page
    affiliate_pattern = r'      <div class="affiliate-resources">.*?</div>\s*</div>\s*</div>'
    
    new_page_content = re.sub(affiliate_pattern, new_section + '\n    </div>\n  </div>', page_content, flags=re.DOTALL)
    
    if new_page_content == page_content:
        print(f"  WARNING: No affiliate section found or replaced for {page_id}")
        return content
    
    return content[:page_start] + new_page_content + content[page_end:]

# Apply replacements
print("Updating affiliate sections...")
for page_id, new_section in REPLACEMENTS.items():
    print(f"  {page_id}...")
    content = find_and_replace_affiliate_section(content, page_id, new_section)

# Write back
with open('index.html', 'w') as f:
    f.write(content)

print("\n✅ Done!")
