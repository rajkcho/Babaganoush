#!/usr/bin/env python3
"""
Add missing calculator functions to pages that had extraction warnings.
"""

import re

# Read index.html to extract the missing functions
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

def extract_function_noindent(content, func_name):
    """Extract a function that doesn't have leading indentation."""
    # Find the function (no leading spaces)
    pattern = rf'\nfunction {re.escape(func_name)}\s*\([^)]*\)\s*{{'
    match = re.search(pattern, content)
    
    if not match:
        return None
    
    start_pos = match.start() + 1
    
    # Find matching closing brace
    brace_count = 0
    in_function = False
    pos = match.end() - 1
    
    for i in range(pos, len(content)):
        char = content[i]
        if char == '{':
            brace_count += 1
            in_function = True
        elif char == '}':
            brace_count -= 1
            if in_function and brace_count == 0:
                end_pos = i + 1
                return content[start_pos:end_pos]
    
    return None

def insert_function_into_page(filename, func_code):
    """Insert calculator function code into a page."""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the insertion point (after "// ═══ CALCULATOR FUNCTIONS ═══")
    marker = '    // ═══ CALCULATOR FUNCTIONS ═══\n'
    insert_pos = content.find(marker)
    
    if insert_pos == -1:
        print(f"  Error: Could not find insertion point in {filename}")
        return False
    
    insert_pos += len(marker)
    
    # Insert the function with proper indentation
    indented_func = '\n    ' + func_code.replace('\n', '\n    ')
    new_content = content[:insert_pos] + indented_func + '\n' + content[insert_pos:]
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

# Fix calculateTFSA
print("Extracting calculateTFSA...")
tfsa_func = extract_function_noindent(index_content, 'calculateTFSA')
if tfsa_func:
    print(f"  Extracted {len(tfsa_func)} bytes")
    print("  Inserting into tfsa-contribution-calculator.html...")
    if insert_function_into_page('tfsa-contribution-calculator.html', tfsa_func):
        print("  ✓ Fixed tfsa-contribution-calculator.html")
else:
    print("  Error: Could not extract calculateTFSA")

# Fix calculateRRSP
print("\nExtracting calculateRRSP...")
rrsp_func = extract_function_noindent(index_content, 'calculateRRSP')
if rrsp_func:
    print(f"  Extracted {len(rrsp_func)} bytes")
    print("  Inserting into rrsp-refund-calculator.html...")
    if insert_function_into_page('rrsp-refund-calculator.html', rrsp_func):
        print("  ✓ Fixed rrsp-refund-calculator.html")
else:
    print("  Error: Could not extract calculateRRSP")

# Fix calculateIncomeTax
print("\nExtracting calculateIncomeTax...")
incometax_func = extract_function_noindent(index_content, 'calculateIncomeTax')
if incometax_func:
    print(f"  Extracted {len(incometax_func)} bytes")
    
    # Also need helper functions
    print("  Extracting helper functions...")
    helpers = []
    for helper_name in ['calcBracketTax', 'getMarginalRate', 'getProvBrackets', 'getProvBasic', 'getProvDTCRate']:
        helper_func = extract_function_noindent(index_content, helper_name)
        if helper_func:
            helpers.append(helper_func)
            print(f"    ✓ {helper_name}")
    
    all_funcs = incometax_func + '\n\n' + '\n\n'.join(helpers)
    
    print("  Inserting into income-tax-calculator.html...")
    if insert_function_into_page('income-tax-calculator.html', all_funcs):
        print("  ✓ Fixed income-tax-calculator.html")
else:
    print("  Error: Could not extract calculateIncomeTax")

# Fix rrsp-tfsa-calculator.html (needs both functions)
print("\nFixing rrsp-tfsa-calculator.html...")
if tfsa_func and rrsp_func:
    combined = tfsa_func + '\n\n' + rrsp_func
    if insert_function_into_page('rrsp-tfsa-calculator.html', combined):
        print("  ✓ Fixed rrsp-tfsa-calculator.html")
else:
    print("  Error: Missing functions")

print("\n" + "="*70)
print("Done!")
