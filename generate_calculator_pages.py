#!/usr/bin/env python3
"""
Generate individual SEO-optimized calculator pages for FiggyBank.ca
"""

import os
import re

# Calculator metadata - Each calculator gets its own page
CALCULATORS = {
    'mortgage': {
        'title': 'Canadian Mortgage Calculator — Free Semi-Annual Compounding',
        'description': 'Free Canadian mortgage calculator with OSFI stress test, CMHC insurance, land transfer tax by province, and full amortization schedule. Compares monthly, bi-weekly, and weekly payments.',
        'emoji': '🏠',
        'url': 'mortgage-calculator',
        'keywords': 'canadian mortgage calculator, mortgage payment calculator canada, CMHC calculator, land transfer tax calculator, mortgage stress test calculator, bi-weekly mortgage calculator',
        'related': ['fhsa', 'rentbuy', 'tax', 'debt'],
    },
    'valuation': {
        'title': 'Business Valuation Calculator — DCF & Multiples',
        'description': 'Free business valuation calculator using DCF (discounted cash flow), revenue multiples, EBITDA multiples, and comparable company analysis. Perfect for startups, SMBs, and M&A.',
        'emoji': '💼',
        'url': 'business-valuation-calculator',
        'keywords': 'business valuation calculator, DCF calculator, EBITDA multiples, SaaS valuation, startup valuation calculator, company valuation',
        'related': ['merger', 'runway', 'investment', 'compound'],
    },
    'investment': {
        'title': 'Investment Returns Calculator — CAGR & Total Return',
        'description': 'Calculate investment returns with CAGR (compound annual growth rate), total return, annualized return, and time-weighted return. Perfect for stocks, ETFs, mutual funds, and portfolios.',
        'emoji': '📈',
        'url': 'investment-returns-calculator',
        'keywords': 'investment calculator canada, CAGR calculator, stock return calculator, portfolio return calculator, annualized return',
        'related': ['compound', 'tfsa', 'rrsp', 'gic'],
    },
    'retirement': {
        'title': 'RRSP vs TFSA Calculator — Optimize Your Retirement Savings',
        'description': 'Compare RRSP vs TFSA contributions, tax savings, and long-term growth. Optimize your retirement strategy with Canadian tax brackets, contribution limits, and withdrawal planning.',
        'emoji': '🏦',
        'url': 'rrsp-tfsa-calculator',
        'keywords': 'rrsp vs tfsa calculator, rrsp calculator canada, tfsa calculator, retirement savings calculator canada, tax refund calculator',
        'related': ['rrsp', 'tfsa', 'cpp', 'resp', 'tax'],
    },
    'compound': {
        'title': 'Compound Interest Calculator — Visualize Your Growth',
        'description': 'Free compound interest calculator with monthly contributions, annual returns, and visual growth chart. See how your savings grow over time with the power of compounding.',
        'emoji': '💹',
        'url': 'compound-interest-calculator',
        'keywords': 'compound interest calculator canada, savings calculator, investment growth calculator, monthly contribution calculator',
        'related': ['investment', 'tfsa', 'rrsp', 'resp'],
    },
    'merger': {
        'title': 'M&A Deal Analyzer — Merger & Acquisition Calculator',
        'description': 'Free M&A calculator for deal analysis, accretion/dilution, synergies, IRR, and post-merger valuation. Perfect for investment bankers, private equity, and business owners.',
        'emoji': '🤝',
        'url': 'merger-acquisition-calculator',
        'keywords': 'M&A calculator, merger calculator, acquisition calculator, accretion dilution calculator, deal analyzer',
        'related': ['valuation', 'runway', 'investment', 'tax'],
    },
    'runway': {
        'title': 'Startup Runway Calculator — Cash Burn & Break-Even',
        'description': 'Calculate startup runway, monthly burn rate, break-even point, and funding needs. Plan your fundraising timeline and optimize cash flow for your startup.',
        'emoji': '🚀',
        'url': 'startup-runway-calculator',
        'keywords': 'startup runway calculator, burn rate calculator, startup cash flow calculator, fundraising calculator, break-even calculator',
        'related': ['valuation', 'merger', 'debt', 'networth'],
    },
    'networth': {
        'title': 'Net Worth Calculator & Tracker — Assets vs Liabilities',
        'description': 'Track your net worth over time with assets, liabilities, and historical snapshots. Compare yourself to Canadian averages by age and income level.',
        'emoji': '💎',
        'url': 'net-worth-calculator',
        'keywords': 'net worth calculator canada, net worth tracker, assets liabilities calculator, financial snapshot',
        'related': ['debt', 'mortgage', 'investment', 'retirement'],
    },
    'lease': {
        'title': 'Lease vs Buy Calculator — Car & Equipment',
        'description': 'Compare leasing vs buying a car or equipment with total cost, depreciation, opportunity cost, and tax implications. Make smarter vehicle and equipment decisions.',
        'emoji': '🚗',
        'url': 'lease-buy-calculator',
        'keywords': 'lease vs buy calculator canada, car lease calculator, vehicle financing calculator, equipment lease calculator',
        'related': ['debt', 'tax', 'compare', 'mortgage'],
    },
    'tax': {
        'title': 'Canadian Tax Estimator — Federal & Provincial 2026',
        'description': 'Quick Canadian tax calculator for 2026 with federal and provincial rates, marginal tax brackets, and take-home pay. All provinces and territories included.',
        'emoji': '💰',
        'url': 'canadian-tax-calculator',
        'keywords': 'canadian tax calculator 2026, income tax calculator canada, marginal tax rate calculator, tax bracket calculator',
        'related': ['incometax', 'salary', 'capgains', 'rrsp'],
    },
    'salary': {
        'title': 'Salary & Compensation Analyzer — Total Comp Calculator',
        'description': 'Calculate total compensation including base salary, bonus, equity, benefits, and perks. Compare job offers and optimize your comp package.',
        'emoji': '💵',
        'url': 'salary-compensation-calculator',
        'keywords': 'salary calculator canada, total compensation calculator, job offer calculator, equity calculator',
        'related': ['tax', 'incometax', 'retirement', 'compare'],
    },
    'debt': {
        'title': 'Debt Payoff Calculator — Snowball vs Avalanche',
        'description': 'Free debt payoff calculator with snowball method, avalanche method, and custom payoff strategies. Calculate interest savings and debt-free date.',
        'emoji': '💳',
        'url': 'debt-payoff-calculator',
        'keywords': 'debt payoff calculator canada, debt snowball calculator, debt avalanche calculator, credit card payoff calculator',
        'related': ['mortgage', 'lease', 'compare', 'networth'],
    },
    'compare': {
        'title': 'Side-by-Side Comparison Calculator',
        'description': 'Compare two financial scenarios side-by-side. Perfect for comparing jobs, investments, loans, or any financial decision.',
        'emoji': '⚖️',
        'url': 'comparison-calculator',
        'keywords': 'financial comparison calculator, side by side calculator, decision calculator',
        'related': ['salary', 'debt', 'lease', 'rentbuy'],
    },
    'currency': {
        'title': 'Currency Converter — Real-Time Exchange Rates',
        'description': 'Free currency converter with real-time exchange rates for CAD, USD, EUR, GBP, and 30+ currencies. Perfect for travel, investments, and international payments.',
        'emoji': '💱',
        'url': 'currency-converter',
        'keywords': 'currency converter, cad to usd, exchange rate calculator, currency calculator',
        'related': ['investment', 'compare', 'tax'],
    },
    'fhsa': {
        'title': 'FHSA Calculator — First Home Savings Account',
        'description': 'Calculate FHSA contributions, tax savings, and growth potential. The FHSA combines RRSP tax deductions with TFSA tax-free withdrawals for first-time home buyers.',
        'emoji': '🏡',
        'url': 'fhsa-calculator',
        'keywords': 'FHSA calculator canada, first home savings account calculator, fhsa vs rrsp, fhsa contribution room',
        'related': ['mortgage', 'rentbuy', 'rrsp', 'tfsa'],
    },
    'resp': {
        'title': 'RESP Calculator — Education Savings with CESG',
        'description': 'Calculate RESP contributions with Canada Education Savings Grant (CESG), provincial grants, and long-term growth. Maximize government grants for your child education.',
        'emoji': '🎓',
        'url': 'resp-calculator',
        'keywords': 'RESP calculator canada, CESG calculator, education savings calculator, RESP contribution calculator',
        'related': ['compound', 'tfsa', 'rrsp', 'tax'],
    },
    'rentbuy': {
        'title': 'Rent vs Buy Calculator — Should You Rent or Buy?',
        'description': 'Compare renting vs buying a home in Canada with total costs, opportunity cost, closing costs, maintenance, and property appreciation. Make a data-driven housing decision.',
        'emoji': '🏘️',
        'url': 'rent-buy-calculator',
        'keywords': 'rent vs buy calculator canada, rent or buy calculator, housing cost calculator, home ownership cost',
        'related': ['mortgage', 'fhsa', 'investment', 'tax'],
    },
    'gic': {
        'title': 'GIC Ladder Calculator — Guaranteed Investment Certificate',
        'description': 'Build and optimize a GIC ladder strategy with different terms, rates, and maturity dates. Maximize returns while maintaining liquidity.',
        'emoji': '🪜',
        'url': 'gic-ladder-calculator',
        'keywords': 'GIC calculator canada, GIC ladder calculator, guaranteed investment certificate calculator, GIC rates',
        'related': ['compound', 'investment', 'tfsa', 'rrsp'],
    },
    'cpp': {
        'title': 'CPP/OAS Calculator — Retirement Income Estimator',
        'description': 'Calculate Canada Pension Plan (CPP) and Old Age Security (OAS) benefits. Optimize when to start taking benefits (age 60, 65, or 70) to maximize lifetime income.',
        'emoji': '👵',
        'url': 'cpp-oas-calculator',
        'keywords': 'CPP calculator canada, OAS calculator, canada pension calculator, CPP benefits calculator, retirement income calculator',
        'related': ['retirement', 'rrsp', 'tfsa', 'tax'],
    },
    'capgains': {
        'title': 'Capital Gains Tax Calculator — Canada 2026',
        'description': 'Calculate capital gains tax on stocks, real estate, and investments in Canada. Includes the 2026 changes to capital gains inclusion rate and principal residence exemption.',
        'emoji': '📊',
        'url': 'capital-gains-calculator',
        'keywords': 'capital gains tax calculator canada 2026, capital gains calculator, investment tax calculator, real estate capital gains',
        'related': ['tax', 'incometax', 'investment', 'tfsa'],
    },
    'tfsa': {
        'title': 'TFSA Contribution Room Calculator — 2026',
        'description': 'Calculate your TFSA contribution room based on age, previous contributions, and withdrawals. Avoid over-contribution penalties and maximize tax-free growth.',
        'emoji': '💼',
        'url': 'tfsa-contribution-calculator',
        'keywords': 'TFSA calculator 2026, TFSA contribution room calculator, TFSA limit calculator, tax free savings account calculator',
        'related': ['retirement', 'rrsp', 'investment', 'compound'],
    },
    'rrsp': {
        'title': 'RRSP Tax Refund Calculator — 2026',
        'description': 'Calculate your RRSP tax refund and contribution room. See how RRSP contributions reduce your taxes across all Canadian provinces and territories.',
        'emoji': '📦',
        'url': 'rrsp-refund-calculator',
        'keywords': 'RRSP calculator 2026, RRSP tax refund calculator, RRSP contribution calculator, registered retirement savings plan',
        'related': ['retirement', 'tfsa', 'tax', 'fhsa'],
    },
    'incometax': {
        'title': 'Canadian Income Tax Calculator — Full 2026 Calculator',
        'description': 'Comprehensive Canadian income tax calculator for 2026 with deductions, credits, RRSP contributions, capital gains, dividends, and detailed tax breakdown by province.',
        'emoji': '🧾',
        'url': 'income-tax-calculator',
        'keywords': 'canadian income tax calculator 2026, tax calculator canada, income tax estimator, tax deductions calculator',
        'related': ['tax', 'rrsp', 'capgains', 'salary'],
    },
}


def generate_seo_content(calc_id, meta):
    """Generate ~500 words of SEO content for each calculator"""
    
    content_templates = {
        'mortgage': '''
<div class="seo-content" style="max-width: 800px; margin: 3rem auto; padding: 0 1rem;">
    <h2>About the Canadian Mortgage Calculator</h2>
    <p>Planning to buy a home in Canada? Our free mortgage calculator helps you estimate your monthly mortgage payments, understand CMHC insurance requirements, calculate land transfer taxes, and pass the OSFI stress test. Whether you're a first-time home buyer or refinancing, this tool provides accurate calculations for all Canadian provinces and territories.</p>
    
    <h3>How Canadian Mortgages Work</h3>
    <p>Unlike the United States, Canadian mortgages use <strong>semi-annual compounding</strong>, not monthly compounding. This means interest is calculated twice per year, which affects your effective interest rate and payment amounts. Our calculator accounts for this Canadian-specific detail to give you accurate payment estimates.</p>
    
    <p>Canadian law requires <strong>CMHC mortgage default insurance</strong> if your down payment is less than 20% of the home's purchase price. This insurance protects the lender (not you) and adds to your monthly payment. Use our calculator to see exactly how much CMHC insurance will cost based on your down payment percentage.</p>
    
    <h3>Understanding the OSFI Stress Test</h3>
    <p>Since 2018, all Canadian homebuyers must qualify for a mortgage at a higher interest rate than they actually pay. This is called the <strong>OSFI stress test</strong>. You must qualify at either your contract rate plus 2%, or 5.25%, whichever is higher. Our calculator shows whether you'll pass the stress test based on your income and debts.</p>
    
    <h3>Land Transfer Tax by Province</h3>
    <p>Most Canadian provinces charge a <strong>land transfer tax</strong> (also called property transfer tax) when you buy a home. The rates vary significantly by province — Ontario and British Columbia have the highest rates, while Alberta has no land transfer tax at all. First-time home buyers may qualify for rebates in Ontario, BC, and PEI. Our calculator shows your exact land transfer tax and any rebates you qualify for.</p>
    
    <h3>Payment Frequency Options</h3>
    <p>Choose from <strong>monthly, bi-weekly, weekly, or semi-monthly</strong> payment frequencies. Bi-weekly and weekly payments result in an extra payment per year (26 bi-weekly payments = 13 monthly payments), which can save you thousands in interest and pay off your mortgage years earlier. Use the comparison chart to see the impact of different payment frequencies.</p>
    
    <h3>Amortization Schedule</h3>
    <p>See exactly how much of each payment goes toward principal vs interest over the life of your mortgage. The amortization schedule shows your balance declining over time, total interest paid, and the breakdown of every payment. Export to PDF or CSV to share with your mortgage broker or financial advisor.</p>
</div>
''',
        'valuation': '''
<div class="seo-content" style="max-width: 800px; margin: 3rem auto; padding: 0 1rem;">
    <h2>Business Valuation Calculator</h2>
    <p>Whether you're buying, selling, or seeking funding, understanding your business's value is critical. Our free business valuation calculator uses industry-standard methods including <strong>DCF (Discounted Cash Flow)</strong>, revenue multiples, EBITDA multiples, and comparable company analysis to estimate your company's worth.</p>
    
    <h3>Valuation Methods Explained</h3>
    <p><strong>Discounted Cash Flow (DCF)</strong> is the gold standard for valuing established businesses with predictable cash flows. It projects future free cash flows and discounts them back to today's dollars using your weighted average cost of capital (WACC). This method is preferred by investment bankers, private equity firms, and professional appraisers.</p>
    
    <p><strong>Revenue multiples</strong> are commonly used for SaaS, tech startups, and high-growth companies that aren't yet profitable. Typical multiples range from 2-10x annual recurring revenue (ARR), depending on growth rate, retention, and market conditions. Our calculator helps you benchmark against industry standards.</p>
    
    <p><strong>EBITDA multiples</strong> work well for profitable, mature businesses. Typical multiples range from 3-8x EBITDA, varying by industry, size, and growth prospects. Manufacturing, distribution, and service businesses are often valued this way.</p>
    
    <h3>When to Get a Professional Valuation</h3>
    <p>While our calculator provides a solid estimate, consider hiring a professional business valuator (CBV in Canada) for: selling your business, buying a business, shareholder disputes, estate planning, divorce proceedings, or seeking institutional investment. Professional valuations cost $5,000-$50,000+ depending on complexity.</p>
    
    <h3>Factors That Impact Value</h3>
    <p>Your valuation depends on: revenue growth rate, profit margins, customer concentration, recurring revenue percentage, market size and trends, competitive advantages, management team strength, and current market conditions. Adjust our calculator's inputs to model different scenarios and see how changes impact value.</p>
</div>
''',
    }
    
    # Use template if exists, else generate generic
    return content_templates.get(calc_id, f'''
<div class="seo-content" style="max-width: 800px; margin: 3rem auto; padding: 0 1rem;">
    <h2>About the {meta['title'].split('—')[0].strip()}</h2>
    <p>Use our free {meta['title'].split('—')[0].strip().lower()} to make smarter financial decisions. This calculator is designed specifically for Canadians, accounting for provincial differences, tax rules, and Canadian financial regulations.</p>
    
    <h3>How to Use This Calculator</h3>
    <p>Enter your financial details in the input fields on the left. Results update instantly as you adjust values. Use the sliders for quick adjustments, or type exact numbers for precision. All calculations happen in your browser—your data never leaves your device.</p>
    
    <h3>Why This Calculator Matters</h3>
    <p>Making informed financial decisions requires accurate calculations and clear comparisons. Our calculator helps you visualize different scenarios, understand the long-term impact of your choices, and optimize your financial strategy. Whether you're planning for retirement, managing debt, or evaluating investments, having the right numbers makes all the difference.</p>
    
    <h3>Privacy & Security</h3>
    <p>FiggyBank calculators run entirely in your browser using JavaScript. No data is sent to our servers, no account required, no tracking. Your financial information stays 100% private. Bookmark this page and use it anytime, completely free.</p>
</div>
''')


def generate_faq_schema(calc_id, meta):
    """Generate FAQ structured data for each calculator"""
    
    faq_templates = {
        'mortgage': [
            {
                "question": "How do Canadian mortgage calculators differ from US calculators?",
                "answer": "Canadian mortgages use semi-annual compounding, while US mortgages use monthly compounding. This means the effective interest rate differs even at the same quoted rate. Canadian calculators must also account for CMHC insurance for down payments under 20%, provincial land transfer taxes, and the OSFI stress test requirement."
            },
            {
                "question": "What is the OSFI mortgage stress test?",
                "answer": "The OSFI stress test requires all Canadian homebuyers to qualify for a mortgage at a higher rate than they actually pay. You must qualify at either your contract rate plus 2% or 5.25%, whichever is higher. This ensures you can still afford payments if rates rise."
            },
            {
                "question": "How much CMHC insurance will I pay?",
                "answer": "CMHC insurance is required for down payments under 20%. The premium ranges from 2.8% (15-19.99% down) to 4% (5-9.99% down) of the mortgage amount. For a $640,000 mortgage with 10% down, CMHC insurance adds approximately $25,600 to your mortgage."
            },
            {
                "question": "Should I choose bi-weekly or monthly mortgage payments?",
                "answer": "Bi-weekly payments result in 26 payments per year (equivalent to 13 monthly payments), helping you pay off your mortgage faster and save on interest. On a $640,000 mortgage at 5.5%, switching to bi-weekly payments can save over $40,000 in interest and reduce your amortization by 2-3 years."
            },
        ],
        'valuation': [
            {
                "question": "What's the difference between revenue multiples and EBITDA multiples?",
                "answer": "Revenue multiples (e.g., 5x annual revenue) are used for high-growth or pre-profitable companies, especially in tech and SaaS. EBITDA multiples (e.g., 6x EBITDA) are used for profitable, mature businesses. SaaS companies might trade at 5-10x revenue, while manufacturing businesses might trade at 4-7x EBITDA."
            },
            {
                "question": "How accurate is a business valuation calculator?",
                "answer": "Online calculators provide reasonable estimates (±20-30%) for typical small to medium businesses. For precise valuations needed for transactions, litigation, or tax purposes, hire a Chartered Business Valuator (CBV). Professional valuations cost $5,000-$50,000+ but provide defensible, certified results."
            },
            {
                "question": "What's a good EBITDA multiple for my industry?",
                "answer": "EBITDA multiples vary by industry: SaaS (8-15x), manufacturing (4-6x), retail (3-5x), professional services (4-8x), restaurants (2-4x). Higher multiples reflect recurring revenue, growth potential, market position, and profitability. Larger companies command higher multiples than smaller ones in the same industry."
            },
        ],
    }
    
    # Use template if exists, else generate generic FAQs
    faqs = faq_templates.get(calc_id, [
        {
            "question": f"How does the {meta['title'].split('—')[0].strip().lower()} work?",
            "answer": f"Our {meta['title'].split('—')[0].strip().lower()} uses Canadian financial rules and tax regulations to provide accurate estimates. Enter your details, and results update instantly. All calculations happen in your browser—no data is sent to our servers."
        },
        {
            "question": "Is this calculator free to use?",
            "answer": "Yes! FiggyBank's calculators are 100% free, with no sign-up required. No ads interrupt your calculations, and your financial data never leaves your device."
        },
        {
            "question": "Can I save or export my results?",
            "answer": "Yes! Click the 'Download PDF Report' button to save your results as a PDF, or use 'Copy Results' to copy to your clipboard. You can also share a link to pre-fill the calculator with your values."
        },
    ])
    
    faq_json = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq["answer"]
                }
            }
            for faq in faqs
        ]
    }
    
    import json
    return json.dumps(faq_json, indent=2)


def extract_calculator_html(calc_id):
    """Extract calculator HTML from index.html"""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the calculator's div
    pattern = rf'<div class="page" id="page-{calc_id}"[^>]*>.*?</div>\s*(?=<div class="page|<!-- ═|$)'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        html = match.group(0)
        # Remove the outer page div and replace with calc-page wrapper
        html = re.sub(r'<div class="page"[^>]*>', '', html, count=1)
        html = html.rstrip('</div>')
        return html
    
    return f'<div class="calc-container"><h1>Calculator: {calc_id}</h1><p>Calculator content goes here.</p></div>'


def generate_calculator_page(calc_id, meta):
    """Generate a complete standalone calculator page"""
    
    # Read styles and scripts
    with open('index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    full_html = ''.join(lines)
    
    # Extract styles (between <style> and </style>)
    style_match = re.search(r'<style>(.*?)</style>', full_html, re.DOTALL)
    styles = style_match.group(1) if style_match else ''
    
    # Extract all JavaScript - Lines 6490 to end (before </body>)
    # This is more reliable than regex for huge files
    script_lines = lines[6489:]  # 0-indexed, so 6489 is line 6490
    # Find where </body> is and stop there
    body_end_idx = -1
    for i, line in enumerate(script_lines):
        if '</body>' in line:
            body_end_idx = i
            break
    
    if body_end_idx > 0:
        scripts = ''.join(script_lines[:body_end_idx])
    else:
        scripts = ''.join(script_lines)
    
    # Get calculator HTML
    calc_html = extract_calculator_html(calc_id)
    
    # Generate related calculator links
    related_html = '<div class="related-calculators" style="max-width: 800px; margin: 2rem auto; padding: 1.5rem; background: var(--glass-bg); border-radius: var(--radius-lg); border: 1px solid var(--border);"><h3 style="margin-top: 0;">Related Calculators</h3><div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">'
    
    for rel_id in meta.get('related', [])[:4]:
        if rel_id in CALCULATORS:
            rel = CALCULATORS[rel_id]
            related_html += f'''
<a href="/{rel['url']}.html" class="related-calc-link" style="padding: 1rem; background: var(--bg-secondary); border-radius: var(--radius-md); text-decoration: none; display: block; transition: transform 0.2s;">
    <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{rel['emoji']}</div>
    <div style="font-weight: 600; color: var(--text-primary);">{rel['title'].split('—')[0].strip()}</div>
</a>
'''
    
    related_html += '</div></div>'
    
    # Generate WebApplication schema
    web_app_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": meta['title'],
        "description": meta['description'],
        "url": f"https://figgybank.ca/{meta['url']}.html",
        "applicationCategory": "FinanceApplication",
        "operatingSystem": "Any",
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "CAD"
        },
        "featureList": "No sign-up required, 100% private, runs in browser, PDF export, share results"
    }
    
    import json
    
    # Build the complete HTML
    html = f'''<!DOCTYPE html>
<html lang="en-CA" class="scroll-smooth">
<head>
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3447886014314572"
     crossorigin="anonymous"></script>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-QHP0GVPV8Q"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-QHP0GVPV8Q');
  </script>
  
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{meta['title']} | FiggyBank</title>
  <meta name="description" content="{meta['description']}" />
  <meta name="keywords" content="{meta['keywords']}" />
  <meta name="robots" content="index, follow" />
  <meta name="author" content="FiggyBank" />
  <meta name="geo.region" content="CA" />
  <meta name="geo.placename" content="Canada" />
  <meta http-equiv="content-language" content="en-CA" />
  
  <!-- Open Graph -->
  <meta property="og:title" content="{meta['title']} | FiggyBank" />
  <meta property="og:description" content="{meta['description']}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://figgybank.ca/{meta['url']}.html" />
  <meta property="og:site_name" content="FiggyBank" />
  <meta property="og:locale" content="en_CA" />
  <meta property="og:image" content="https://figgybank.ca/og-image.png" />
  
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{meta['title']}" />
  <meta name="twitter:description" content="{meta['description']}" />
  
  <link rel="canonical" href="https://figgybank.ca/{meta['url']}.html" />
  <link rel="alternate" hreflang="en-ca" href="https://figgybank.ca/{meta['url']}.html" />
  
  <!-- Preconnect -->
  <link rel="preconnect" href="https://www.googletagmanager.com" />
  <link rel="dns-prefetch" href="https://www.googletagmanager.com" />
  <link rel="dns-prefetch" href="https://fonts.googleapis.com" />
  <link rel="dns-prefetch" href="https://fonts.gstatic.com" />

  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet" />

  <meta name="theme-color" content="#2C087D" />
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🐷</text></svg>" />

  <!-- Structured Data: WebApplication -->
  <script type="application/ld+json">
{json.dumps(web_app_schema, indent=2)}
  </script>

  <!-- Structured Data: FAQPage -->
  <script type="application/ld+json">
{generate_faq_schema(calc_id, meta)}
  </script>

  <!-- Structured Data: BreadcrumbList -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://figgybank.ca/"}},
      {{"@type": "ListItem", "position": 2, "name": "{meta['title'].split('—')[0].strip()}", "item": "https://figgybank.ca/{meta['url']}.html"}}
    ]
  }}
  </script>

  <!-- PDF Export Libraries -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js" integrity="sha512-BNaRQnYJYiPSqHHDb58B0yaPfCu+Wgds8Gp/gU33kqBtgNS4tSPHuGibyoeqMV/TJlSKda6FXzoEyYGjTe+vXA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js" crossorigin="anonymous" referrerpolicy="no-referrer"></script>

  <style>
{styles}
  </style>
</head>
<body>
  <a href="#main-content" class="skip-to-content">Skip to main content</a>
  <div id="scroll-progress"></div>

  <!-- ══ NAVIGATION ══ -->
  <nav class="nav-bar" id="navbar">
    <div class="nav-inner">
      <a href="/" class="nav-logo">
        <svg class="nav-logo-svg" width="36" height="36" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
          <ellipse cx="32" cy="36" rx="22" ry="18" fill="#FF8A8A"/>
          <ellipse cx="32" cy="36" rx="22" ry="18" fill="url(#piggyGrad)" opacity="0.5"/>
          <ellipse cx="16" cy="22" rx="6" ry="7" fill="#FF8A8A" transform="rotate(-15 16 22)"/>
          <ellipse cx="16" cy="22" rx="4" ry="5" fill="#FFB5B5" transform="rotate(-15 16 22)"/>
          <ellipse cx="48" cy="22" rx="6" ry="7" fill="#FF8A8A" transform="rotate(15 48 22)"/>
          <ellipse cx="48" cy="22" rx="4" ry="5" fill="#FFB5B5" transform="rotate(15 48 22)"/>
          <rect x="26" y="19" width="12" height="3" rx="1.5" fill="#F5A623"/>
          <rect x="27" y="20" width="10" height="1" rx="0.5" fill="#D4891A"/>
          <ellipse cx="32" cy="40" rx="8" ry="6" fill="#FFB5B5"/>
          <circle cx="29" cy="39.5" r="1.5" fill="#E88A8A"/>
          <circle cx="35" cy="39.5" r="1.5" fill="#E88A8A"/>
          <circle cx="24" cy="32" r="2.5" fill="#2C087D"/>
          <circle cx="40" cy="32" r="2.5" fill="#2C087D"/>
          <circle cx="25" cy="31" r="1" fill="white"/>
          <circle cx="41" cy="31" r="1" fill="white"/>
          <path d="M28 43 Q32 46 36 43" stroke="#E88A8A" stroke-width="1.5" fill="none" stroke-linecap="round"/>
          <rect x="20" y="50" width="5" height="6" rx="2.5" fill="#FF8A8A"/>
          <rect x="39" y="50" width="5" height="6" rx="2.5" fill="#FF8A8A"/>
          <path d="M54 34 Q58 30 56 26 Q54 22 58 20" stroke="#FF8A8A" stroke-width="2.5" fill="none" stroke-linecap="round"/>
          <defs>
            <linearGradient id="piggyGrad" x1="10" y1="18" x2="54" y2="54">
              <stop offset="0%" stop-color="#FFD4D4"/>
              <stop offset="100%" stop-color="#FF6B6B" stop-opacity="0.3"/>
            </linearGradient>
          </defs>
        </svg>
        <span>FiggyBank</span>
      </a>
      
      <ul class="nav-links" id="nav-links">
        <li><a href="/">Home</a></li>
        <li class="nav-dropdown">
          <a href="#" class="nav-dropdown-trigger" onclick="return false;">Calculators <span style="font-size:0.6em;margin-left:2px;">▾</span></a>
          <div class="nav-dropdown-menu">
            <div class="nav-dropdown-grid">
              <div class="nav-dropdown-group">
                <span class="nav-dropdown-label">🏠 Home & Property</span>
                <a href="/mortgage-calculator.html">Mortgage</a>
                <a href="/fhsa-calculator.html">FHSA</a>
                <a href="/rent-buy-calculator.html">Rent vs Buy</a>
                <a href="/lease-buy-calculator.html">Lease vs Buy</a>
              </div>
              <div class="nav-dropdown-group">
                <span class="nav-dropdown-label">💰 Tax & Income</span>
                <a href="/canadian-tax-calculator.html">Tax Estimator</a>
                <a href="/income-tax-calculator.html">Full Income Tax</a>
                <a href="/capital-gains-calculator.html">Capital Gains</a>
                <a href="/salary-compensation-calculator.html">Salary</a>
              </div>
              <div class="nav-dropdown-group">
                <span class="nav-dropdown-label">📈 Investing & Savings</span>
                <a href="/tfsa-contribution-calculator.html">TFSA Room</a>
                <a href="/investment-returns-calculator.html">Investment Returns</a>
                <a href="/compound-interest-calculator.html">Compound Interest</a>
                <a href="/gic-ladder-calculator.html">GIC Ladder</a>
                <a href="/currency-converter.html">Currency</a>
              </div>
              <div class="nav-dropdown-group">
                <span class="nav-dropdown-label">🏦 Retirement</span>
                <a href="/rrsp-refund-calculator.html">RRSP Refund</a>
                <a href="/rrsp-tfsa-calculator.html">RRSP vs TFSA</a>
                <a href="/resp-calculator.html">RESP</a>
                <a href="/cpp-oas-calculator.html">CPP/OAS</a>
              </div>
              <div class="nav-dropdown-group">
                <span class="nav-dropdown-label">🏢 Business & Debt</span>
                <a href="/business-valuation-calculator.html">Valuation</a>
                <a href="/merger-acquisition-calculator.html">M&A Analyzer</a>
                <a href="/startup-runway-calculator.html">Startup Runway</a>
                <a href="/debt-payoff-calculator.html">Debt Payoff</a>
                <a href="/net-worth-calculator.html">Net Worth</a>
                <a href="/comparison-calculator.html">Compare</a>
              </div>
            </div>
          </div>
        </li>
        <li class="nav-dropdown">
          <a href="#" class="nav-dropdown-trigger" onclick="return false;">Tools <span style="font-size:0.6em;margin-left:2px;">▾</span></a>
          <div class="nav-dropdown-menu">
            <div class="nav-dropdown-grid">
              <div class="nav-dropdown-group">
                <span class="nav-dropdown-label">🧭 Interactive</span>
                <a href="/quiz.html">Financial Health Quiz</a>
                <a href="/benchmarks.html">How Do You Compare?</a>
                <a href="/cost-of-living.html">Cost of Living</a>
              </div>
              <div class="nav-dropdown-group">
                <span class="nav-dropdown-label">📋 Resources</span>
                <a href="/checklists.html">Life Checklists</a>
                <a href="/glossary.html">Financial Glossary</a>
              </div>
            </div>
          </div>
        </li>
        <li><a href="/blog/">Blog</a></li>
      </ul>
      
      <div class="nav-actions">
        <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle theme">☀️</button>
        <button class="mobile-menu-btn" onclick="toggleMobileMenu()" aria-label="Menu">☰</button>
      </div>
    </div>
  </nav>

  <main id="main-content">
    {calc_html}
    
    {generate_seo_content(calc_id, meta)}
    
    {related_html}
  </main>

  <!-- ══ FOOTER ══ -->
  <footer class="figgy-footer">
    <div class="footer-content">
      <div class="footer-section">
        <h3>FiggyBank</h3>
        <p>Free Canadian financial calculators — smart money moves made simple.</p>
        <div class="footer-social">
          <a href="https://twitter.com/FiggyBankCA" aria-label="Twitter">🐦</a>
        </div>
      </div>
      
      <div class="footer-section">
        <h4>Calculators</h4>
        <ul>
          <li><a href="/mortgage-calculator.html">Mortgage Calculator</a></li>
          <li><a href="/business-valuation-calculator.html">Business Valuation</a></li>
          <li><a href="/rrsp-tfsa-calculator.html">RRSP vs TFSA</a></li>
          <li><a href="/canadian-tax-calculator.html">Tax Calculator</a></li>
          <li><a href="/cpp-oas-calculator.html">CPP/OAS Calculator</a></li>
        </ul>
      </div>
      
      <div class="footer-section">
        <h4>Resources</h4>
        <ul>
          <li><a href="/blog/">Blog</a></li>
          <li><a href="/glossary.html">Financial Glossary</a></li>
          <li><a href="/quiz.html">Financial Health Quiz</a></li>
          <li><a href="/checklists.html">Life Checklists</a></li>
        </ul>
      </div>
      
      <div class="footer-section">
        <h4>Legal</h4>
        <ul>
          <li><a href="/#privacy">Privacy Policy</a></li>
          <li><a href="/#disclaimer">Disclaimer</a></li>
        </ul>
        <p style="font-size: 0.75rem; margin-top: 1rem; opacity: 0.7;">
          © 2026 FiggyBank.ca · Made in Canada 🇨🇦
        </p>
      </div>
    </div>
  </footer>

  {scripts}

  <script>
    // Initialize calculator on page load
    document.addEventListener('DOMContentLoaded', function() {{
      // Auto-run the calculator's init function
      const calcFunctions = {{
        'valuation': 'calculateDCF',
        'mortgage': 'calculateMortgage',
        'investment': 'calculateCAGR',
        'retirement': 'calculateRetirement',
        'compound': 'calculateCompound',
        'runway': 'calculateRunway',
        'networth': 'calculateNetWorth',
        'salary': 'calculateSalary',
        'debt': 'calculateDebt',
        'compare': 'calculateComparison',
        'currency': 'convertCurrency',
        'lease': 'calculateLeaseBuy',
        'tax': 'calculateTax',
        'fhsa': 'calculateFHSA',
        'resp': 'calculateRESP',
        'rentbuy': 'calculateRentBuy',
        'gic': 'calculateGIC',
        'cpp': 'calculateCPP',
        'capgains': 'calculateCapGains',
        'tfsa': 'calculateTFSA',
        'rrsp': 'calculateRRSP',
        'incometax': 'calculateIncomeTax'
      }};
      
      const calcId = '{calc_id}';
      const funcName = calcFunctions[calcId];
      
      if (funcName && typeof window[funcName] === 'function') {{
        window[funcName]();
      }}
      
      // For net worth, also load snapshots
      if (calcId === 'networth' && typeof loadNetWorthSnapshots === 'function') {{
        loadNetWorthSnapshots();
      }}
    }});
  </script>
</body>
</html>
'''
    
    return html


def main():
    """Generate all calculator pages"""
    os.chdir('/home/openclaw/.openclaw/workspace/figgybank')
    
    print(f"🚀 Generating {len(CALCULATORS)} calculator pages...")
    
    for calc_id, meta in CALCULATORS.items():
        filename = f"{meta['url']}.html"
        print(f"  📄 Creating {filename}...")
        
        try:
            html = generate_calculator_page(calc_id, meta)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"  ✅ {filename} created successfully")
        except Exception as e:
            print(f"  ❌ Error creating {filename}: {e}")
    
    print("\n✅ All calculator pages generated!")
    print(f"\n📋 Next steps:")
    print(f"  1. Update sitemap.xml with all new pages")
    print(f"  2. Update index.html to link to individual pages")
    print(f"  3. Test a few pages locally")
    print(f"  4. Push to GitHub")

if __name__ == '__main__':
    main()
