#!/usr/bin/env python3
"""
Script to update affiliate sections with expanded product lists
"""

# Product database - ASIN mappings
PRODUCTS = {
    'wealthyBarber': ('0143190008', 'The Wealthy Barber Returns', 'David Chilton'),
    'tfsa': ('1459721646', 'Tax-Free Savings Accounts', 'Gordon Pape'),
    'howNot': ('0143191292', 'How NOT to Move Back in with Your Parents', 'Rob Chicken'),
    'millionaire': ('1119356296', 'Millionaire Teacher', 'Andrew Hallam'),
    'wealthing': ('0993874177', 'Wealthing Like Rabbits', 'Robert R. Brown'),
    'commonSense': ('1119404509', 'The Little Book of Common Sense Investing', 'John C. Bogle'),
    'moneyMakeover': ('1595555277', 'The Total Money Makeover', 'Dave Ramsey'),
    'builtToSell': ('1591845823', 'Built to Sell', 'John Warrillow'),
    'artOfSelling': ('1733478159', 'The Art of Selling Your Business', 'John Warrillow'),
    'wealthyRenter': ('B01MFAQMJS', 'The Wealthy Renter', 'Alex Avery'),
    'yourMoney': ('0143115766', 'Your Money or Your Life', 'Vicki Robin'),
    'randomWalk': ('0393358380', 'A Random Walk Down Wall Street', 'Burton Malkiel'),
    'victoryLap': ('1988344305', 'Victory Lap Retirement', 'Mike Drak'),
    'pensionize': ('1118691342', 'Pensionize Your Nest Egg', 'Moshe Milevsky'),
    'neverSplit': ('0062407805', 'Never Split the Difference', 'Chris Voss'),
    'quitLike': ('0525538690', 'Quit Like a Millionaire', 'Kristy Shen'),
    'teachRich': ('1523505745', 'I Will Teach You to Be Rich', 'Ramit Sethi'),
    'leanStartup': ('0307887898', 'The Lean Startup', 'Eric Ries'),
    'zeroToOne': ('0804139296', 'Zero to One', 'Peter Thiel'),
    'baiiPlus': ('B00000JZKB', 'Texas Instruments BA II Plus Calculator', ''),
    'intelligentInvestor': ('0060555661', 'The Intelligent Investor', 'Benjamin Graham'),
    'richDad': ('1612680194', 'Rich Dad Poor Dad', 'Robert Kiyosaki'),
    'psychologyMoney': ('0857197681', 'The Psychology of Money', 'Morgan Housel'),
    'bondBook': ('070716647X', 'The Bond Book', 'Annette Thau'),
}

# Affiliate recommendations per calculator with custom pitches
RECOMMENDATIONS = {
    'capgains': [
        ('millionaire', 'Tax-efficient investing strategies for Canadians'),
        ('tfsa', 'Shelter capital gains in your TFSA'),
        ('intelligentInvestor', 'Understanding value and capital appreciation'),
        ('commonSense', 'Index investing for lower turnover and taxes'),
        ('psychologyMoney', 'Long-term thinking for capital gains success'),
    ],
    'cpp': [
        ('victoryLap', 'Plan your CPP timing with retirement strategy'),
        ('pensionize', 'Create guaranteed income streams alongside CPP'),
        ('wealthyBarber', 'Canadian retirement planning essentials'),
        ('millionaire', 'Building wealth beyond government benefits'),
        ('yourMoney', 'Financial independence and retirement planning'),
    ],
    'debt': [
        ('moneyMakeover', 'The proven debt snowball method'),
        ('quitLike', 'Achieve financial independence after debt'),
        ('wealthing', 'Canadian perspective on debt-free living'),
        ('yourMoney', 'Transform your relationship with money'),
        ('teachRich', 'Automate your way out of debt'),
    ],
    'incometax': [
        ('wealthyBarber', 'Tax-smart wealth building for Canadians'),
        ('tfsa', 'Maximize tax-free growth opportunities'),
        ('howNot', 'Young professional tax strategies'),
        ('teachRich', 'Tax-efficient automation and investing'),
        ('psychologyMoney', 'Smart money decisions and tax planning'),
    ],
    'rentbuy': [
        ('wealthyRenter', 'The financial case for renting vs buying'),
        ('yourMoney', 'True cost of homeownership analysis'),
        ('wealthyBarber', 'Canadian housing and wealth building'),
        ('millionaire', 'Building wealth regardless of housing choice'),
        ('psychologyMoney', 'Emotional vs rational home buying decisions'),
    ],
    'resp': [
        ('wealthyBarber', 'Family financial planning in Canada'),
        ('tfsa', 'Tax-advantaged savings for education'),
        ('howNot', 'Setting up your kids for financial success'),
        ('teachRich', 'Automated savings for education goals'),
        ('psychologyMoney', 'Teaching kids about money and investing'),
    ],
    'retirement': [
        ('victoryLap', 'Redefine retirement on your terms'),
        ('pensionize', 'Turn savings into guaranteed retirement income'),
        ('millionaire', 'Building a portfolio for retirement'),
        ('wealthyBarber', 'Canadian retirement essentials'),
        ('yourMoney', 'Achieve financial independence'),
    ],
    'rrsp': [
        ('wealthyBarber', 'RRSP strategies for Canadians'),
        ('tfsa', 'RRSP vs TFSA decision making'),
        ('howNot', 'Early-career retirement savings'),
        ('teachRich', 'Automate your RRSP contributions'),
        ('psychologyMoney', 'Long-term thinking for retirement'),
    ],
    'runway': [
        ('leanStartup', 'Build and pivot before you run out of runway'),
        ('zeroToOne', 'Create breakthrough value quickly'),
        ('builtToSell', 'Build a business that generates cash'),
        ('artOfSelling', 'Know your exit options early'),
        ('richDad', 'Entrepreneurial cashflow thinking'),
    ],
    'salary': [
        ('neverSplit', 'Master salary negotiation tactics'),
        ('wealthyBarber', 'Make the most of your income'),
        ('howNot', 'Young professional compensation guide'),
        ('teachRich', 'Optimize and automate your salary'),
        ('psychologyMoney', 'Career and compensation mindset'),
    ],
    'tfsa': [
        ('tfsa', 'The complete guide to TFSAs'),
        ('wealthyBarber', 'Canadian tax-free investing strategies'),
        ('howNot', 'TFSA strategies for young Canadians'),
        ('teachRich', 'Automate your TFSA contributions'),
        ('commonSense', 'Simple index investing in your TFSA'),
    ],
}

def generate_affiliate_card(product_key, pitch):
    """Generate HTML for a single affiliate card"""
    asin, title, author = PRODUCTS[product_key]
    author_html = f'<span class="affiliate-author">{author}</span>' if author else ''
    
    return f'''          <a href="https://www.amazon.ca/dp/{asin}?tag=figgy0a0-20" target="_blank" rel="noopener noreferrer sponsored" class="affiliate-card">
            <div class="affiliate-info">
              <span class="affiliate-title">{title}</span>
              {author_html}
              <span class="affiliate-why">{pitch}</span>
            </div>
          </a>'''

def generate_affiliate_section(calc_id):
    """Generate complete affiliate-resources section for a calculator"""
    if calc_id not in RECOMMENDATIONS:
        return None
    
    cards = '\n'.join(generate_affiliate_card(prod, pitch) 
                     for prod, pitch in RECOMMENDATIONS[calc_id])
    
    return f'''      <div class="affiliate-resources">
        <h3>📚 Recommended Resources</h3>
        <div class="affiliate-grid">
{cards}
        </div>
        <p class="affiliate-disclosure">As an Amazon Associate, FiggyBank earns from qualifying purchases.</p>
      </div>'''

# Print sections for manual verification
for calc_id in sorted(RECOMMENDATIONS.keys()):
    print(f"\n{'='*60}")
    print(f"{calc_id.upper()} ({len(RECOMMENDATIONS[calc_id])} cards)")
    print('='*60)
    print(generate_affiliate_section(calc_id))
