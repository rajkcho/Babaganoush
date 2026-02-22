#!/usr/bin/env python3
"""Merge RRSP vs TFSA Pro into the existing retirement page, remove the Pro page"""

with open('index.html', 'r') as f:
    content = f.read()

# 1. Read the rrsptfsa HTML and adapt it to replace retirement
# Find rrsptfsa page
import re

rrsptfsa_match = re.search(
    r'<div class="page" id="page-rrsptfsa".*?(?=\n\n  <!-- ═)',
    content, re.DOTALL
)
rrsptfsa_html = rrsptfsa_match.group(0)

# Change id to page-retirement
rrsptfsa_html = rrsptfsa_html.replace('id="page-rrsptfsa"', 'id="page-retirement"')
# Update share links
rrsptfsa_html = rrsptfsa_html.replace("shareCalculator('rrsptfsa')", "shareCalculator('retirement')")

# 2. Replace old retirement page with adapted rrsptfsa
retirement_match = re.search(
    r'<div class="page" id="page-retirement".*?</div>\s*\n\s*<!-- ═+\s*COMPOUND INTEREST',
    content, re.DOTALL
)
old_retirement = retirement_match.group(0)
# Keep the compound interest comment
compound_comment_idx = old_retirement.index('<!-- ═')
trailing = old_retirement[compound_comment_idx:]

content = content.replace(old_retirement, rrsptfsa_html + '\n\n  ' + trailing)

# 3. Remove the now-duplicate rrsptfsa page
content = re.sub(
    r'\n\s*<!-- RRSP vs TFSA Comparison Tool -->\s*\n<div class="page" id="page-rrsptfsa".*?(?=\n\n  <!-- ═)',
    '',
    content, flags=re.DOTALL
)
# Also try without the comment
content = re.sub(
    r'\n<div class="page" id="page-rrsptfsa".*?</div>\s*</div>\s*</div>\s*\n',
    '\n',
    content, flags=re.DOTALL
)

# 4. Replace calculateRRSPvsTFSA references with calculateRetirement
# First, rename the function
content = content.replace('function calculateRRSPvsTFSA()', 'function calculateRetirement()')
content = content.replace("calculateRRSPvsTFSA()", "calculateRetirement()")

# Remove old calculateRetirement function
old_ret_match = re.search(r'function calculateRetirement\(\) \{', content)
if old_ret_match:
    # Find the FIRST one (old) and remove it
    pos = old_ret_match.start()
    # Count braces to find end
    brace_count = 0
    i = pos
    found_first = False
    while i < len(content):
        if content[i] == '{':
            brace_count += 1
            found_first = True
        elif content[i] == '}':
            brace_count -= 1
            if found_first and brace_count == 0:
                end_pos = i + 1
                break
        i += 1
    
    # Check if there's a second one (the renamed one)
    second_match = re.search(r'function calculateRetirement\(\) \{', content[end_pos:])
    if second_match:
        # Remove the first (old) one
        content = content[:pos] + content[end_pos:]
        print("Removed old calculateRetirement, kept new one")
    else:
        print("Only one calculateRetirement found, keeping it")

# 5. Remove rrsptfsa from nav
content = content.replace(
    """                <a href="#" onclick="showPage('rrsptfsa'); return false;">RRSP vs TFSA Pro</a>\n""",
    ''
)
# Also remove from showPage init blocks
content = content.replace("      if (pageId === 'rrsptfsa') calculateRetirement();\n", '')
content = content.replace("            if (pageId === 'rrsptfsa') calculateRetirement();\n", '')

# 6. Update nav label - rename "RRSP vs TFSA" to something clearer
content = content.replace(
    """<a href="#" onclick="showPage('retirement'); return false;">RRSP vs TFSA</a>""",
    """<a href="#" onclick="showPage('retirement'); return false;">RRSP vs TFSA</a>"""
)

with open('index.html', 'w') as f:
    f.write(content)

print(f"Done! {len(content.splitlines())} lines")
# Verify
count_retirement = content.count('page-retirement')
count_rrsptfsa = content.count('page-rrsptfsa')
print(f"page-retirement refs: {count_retirement}")
print(f"page-rrsptfsa refs: {count_rrsptfsa} (should be 0)")
