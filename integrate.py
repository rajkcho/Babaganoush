#!/usr/bin/env python3
"""Integrate Tier 1 calculator snippets into FiggyBank index.html"""
import re

with open('index.html', 'r') as f:
    html = f.read()

lines = html.split('\n')

# === 1. Replace capgains HTML (lines 5712-5793) with new capgains + new pages ===
# Find capgains page start and end
capgains_start = None
capgains_end = None
for i, line in enumerate(lines):
    if 'id="page-capgains"' in line:
        capgains_start = i
    if capgains_start and i > capgains_start and 'JAVASCRIPT ENGINE' in line:
        # Go back to find the closing </div> of capgains
        for j in range(i-1, capgains_start, -1):
            if '</div>' in lines[j]:
                capgains_end = j
                break
        break

print(f"Capgains page: lines {capgains_start+1}-{capgains_end+1}")

# Read snippet files
snippets = {}
for name in ['capgains-html', 'tfsa-html', 'rrsp-html', 'incometax-html', 'rrsptfsa-html',
             'capgains-js', 'tfsa-js', 'rrsp-js', 'incometax-js', 'rrsptfsa-js']:
    with open(f'snippets/{name}.html' if 'html' in name else f'snippets/{name}.js', 'r') as f:
        snippets[name] = f.read()

# Build new HTML pages block
new_pages = '\n'.join([
    snippets['capgains-html'],
    '',
    '  <!-- TFSA Contribution Room Calculator -->',
    snippets['tfsa-html'],
    '',
    '  <!-- RRSP Tax Refund Calculator -->',
    snippets['rrsp-html'],
    '',
    '  <!-- Canadian Income Tax Calculator -->',
    snippets['incometax-html'],
    '',
    '  <!-- RRSP vs TFSA Comparison Tool -->',
    snippets['rrsptfsa-html'],
])

# Replace capgains page with all new pages
new_lines = lines[:capgains_start] + new_pages.split('\n') + lines[capgains_end+1:]

# === 2. Insert JS functions before the closing </script> ===
# Find the main script's calculateCapGains function and replace it
html_new = '\n'.join(new_lines)

# Replace the old calculateCapGains function
# Find it and its end
old_capgains_match = re.search(r'function calculateCapGains\(\) \{', html_new)
if old_capgains_match:
    start_pos = old_capgains_match.start()
    # Find the end by counting braces
    brace_count = 0
    pos = start_pos
    found_first = False
    while pos < len(html_new):
        if html_new[pos] == '{':
            brace_count += 1
            found_first = True
        elif html_new[pos] == '}':
            brace_count -= 1
            if found_first and brace_count == 0:
                end_pos = pos + 1
                break
        pos += 1
    
    # Replace old capgains with new capgains + all new functions
    new_js = '\n'.join([
        snippets['capgains-js'],
        '',
        '    // ═══ TFSA CONTRIBUTION ROOM CALCULATOR ═══',
        snippets['tfsa-js'],
        '',
        '    // ═══ RRSP TAX REFUND CALCULATOR ═══',
        snippets['rrsp-js'],
        '',
        '    // ═══ CANADIAN INCOME TAX CALCULATOR ═══',
        snippets['incometax-js'],
        '',
        '    // ═══ RRSP VS TFSA COMPARISON TOOL ═══',
        snippets['rrsptfsa-js'],
    ])
    
    html_new = html_new[:start_pos] + new_js + html_new[end_pos:]
    print("Replaced calculateCapGains and added new JS functions")

# === 3. Update nav menu - add new calculators ===
# Add TFSA and Income Tax to the nav
nav_replacement = '''                <span class="nav-dropdown-label">💰 Tax & Income</span>
                <a href="#" onclick="showPage('tax'); return false;">Tax Estimator</a>
                <a href="#" onclick="showPage('incometax'); return false;">Full Income Tax</a>
                <a href="#" onclick="showPage('capgains'); return false;">Capital Gains</a>
                <a href="#" onclick="showPage('salary'); return false;">Salary</a>'''

html_new = html_new.replace(
    '''                <span class="nav-dropdown-label">💰 Tax & Income</span>
                <a href="#" onclick="showPage('tax'); return false;">Tax Estimator</a>
                <a href="#" onclick="showPage('capgains'); return false;">Capital Gains</a>
                <a href="#" onclick="showPage('salary'); return false;">Salary</a>''',
    nav_replacement
)

# Add TFSA to Investing & Savings
html_new = html_new.replace(
    '''                <span class="nav-dropdown-label">📈 Investing & Savings</span>
                <a href="#" onclick="showPage('investment'); return false;">Investment Returns</a>''',
    '''                <span class="nav-dropdown-label">📈 Investing & Savings</span>
                <a href="#" onclick="showPage('tfsa'); return false;">TFSA Room</a>
                <a href="#" onclick="showPage('investment'); return false;">Investment Returns</a>'''
)

# Add RRSP refund and RRSP vs TFSA to Retirement
html_new = html_new.replace(
    '''                <span class="nav-dropdown-label">🏦 Retirement</span>
                <a href="#" onclick="showPage('retirement'); return false;">RRSP vs TFSA</a>''',
    '''                <span class="nav-dropdown-label">🏦 Retirement</span>
                <a href="#" onclick="showPage('rrsp'); return false;">RRSP Refund</a>
                <a href="#" onclick="showPage('rrsptfsa'); return false;">RRSP vs TFSA Pro</a>
                <a href="#" onclick="showPage('retirement'); return false;">RRSP vs TFSA</a>'''
)

# === 4. Update showPage functions ===
# First showPage (around line 7195)
showpage_addition = """      if (pageId === 'capgains') calculateCapGains();
      if (pageId === 'tfsa') calculateTFSA();
      if (pageId === 'rrsp') calculateRRSP();
      if (pageId === 'incometax') calculateIncomeTax();
      if (pageId === 'rrsptfsa') calculateRRSPvsTFSA();"""

html_new = html_new.replace(
    "      if (pageId === 'capgains') calculateCapGains();\n    }",
    showpage_addition + "\n    }",
    1
)

# Second showPage (transition wrapper)
showpage_addition2 = """            if (pageId === 'capgains') calculateCapGains();
            if (pageId === 'tfsa') calculateTFSA();
            if (pageId === 'rrsp') calculateRRSP();
            if (pageId === 'incometax') calculateIncomeTax();
            if (pageId === 'rrsptfsa') calculateRRSPvsTFSA();"""

html_new = html_new.replace(
    "            if (pageId === 'capgains') calculateCapGains();\n          }, 150);",
    showpage_addition2 + "\n          }, 150);",
    1
)

# === 5. Write output ===
with open('index.html', 'w') as f:
    f.write(html_new)

new_count = len(html_new.split('\n'))
print(f"Done! index.html now has {new_count} lines")
