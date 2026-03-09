#!/usr/bin/env python3
"""
Fix all 23 calculator pages by replacing the bloated ~8000-line script with only
the necessary JavaScript for each calculator.
"""

import re
import os

# Map of calculator page names to their function names and line ranges in index.html
CALCULATOR_MAP = {
    'fhsa-calculator.html': {
        'calc_id': 'fhsa',
        'func_name': 'calculateFHSA',
        'func_pattern': r'function calculateFHSA\(\)',
    },
    'resp-calculator.html': {
        'calc_id': 'resp',
        'func_name': 'calculateRESP',
        'func_pattern': r'function calculateRESP\(\)',
    },
    'rent-buy-calculator.html': {
        'calc_id': 'rentbuy',
        'func_name': 'calculateRentBuy',
        'func_pattern': r'function calculateRentBuy\(\)',
    },
    'gic-ladder-calculator.html': {
        'calc_id': 'gic',
        'func_name': 'calculateGIC',
        'func_pattern': r'function calculateGIC\(\)',
    },
    'cpp-oas-calculator.html': {
        'calc_id': 'cpp',
        'func_name': 'calculateCPP',
        'func_pattern': r'function calculateCPP\(\)',
    },
    'capital-gains-calculator.html': {
        'calc_id': 'capgains',
        'func_name': 'calculateCapGains',
        'func_pattern': r'function calculateCapGains\(\)',
    },
    'tfsa-contribution-calculator.html': {
        'calc_id': 'tfsa',
        'func_name': 'calculateTFSA',
        'func_pattern': r'function calculateTFSA\(\)',
    },
    'rrsp-tfsa-calculator.html': {
        'calc_id': 'retirement',
        'func_name': 'calculateRRSP',
        'func_pattern': r'function calculateRRSP\(\)',
    },
    'income-tax-calculator.html': {
        'calc_id': 'incometax',
        'func_name': 'calculateIncomeTax',
        'func_pattern': r'function calculateIncomeTax\(\)',
    },
    'business-valuation-calculator.html': {
        'calc_id': 'valuation',
        'func_name': 'calculateDCF',
        'func_pattern': r'function calculateDCF\(\)',
        'extra_funcs': ['calculateMultiples', 'calculateAsset', 'setIndustryPreset'],
    },
    'mortgage-calculator.html': {
        'calc_id': 'mortgage',
        'func_name': 'calculateMortgage',
        'func_pattern': r'function calculateMortgage\(\)',
    },
    'investment-returns-calculator.html': {
        'calc_id': 'investment',
        'func_name': 'calculateCAGR',
        'func_pattern': r'function calculateCAGR\(\)',
        'extra_funcs': ['calculateDCA', 'calculateRetirement'],
    },
    'compound-interest-calculator.html': {
        'calc_id': 'compound',
        'func_name': 'calculateCompound',
        'func_pattern': r'function calculateCompound\(\)',
    },
    'merger-acquisition-calculator.html': {
        'calc_id': 'merger',
        'func_name': 'calculateMA',
        'func_pattern': r'function calculateMA\(\)',
    },
    'startup-runway-calculator.html': {
        'calc_id': 'runway',
        'func_name': 'calculateRunway',
        'func_pattern': r'function calculateRunway\(\)',
        'extra_funcs': ['addHireRow'],
    },
    'net-worth-calculator.html': {
        'calc_id': 'networth',
        'func_name': 'calculateNetWorth',
        'func_pattern': r'function calculateNetWorth\(\)',
        'extra_funcs': ['loadNetWorthSnapshots', 'saveNetWorthSnapshot', 'deleteSnapshot'],
    },
    'salary-compensation-calculator.html': {
        'calc_id': 'salary',
        'func_name': 'calculateSalary',
        'func_pattern': r'function calculateSalary\(\)',
    },
    'debt-payoff-calculator.html': {
        'calc_id': 'debt',
        'func_name': 'calculateDebt',
        'func_pattern': r'function calculateDebt\(\)',
    },
    'comparison-calculator.html': {
        'calc_id': 'compare',
        'func_name': 'calculateComparison',
        'func_pattern': r'function calculateComparison\(\)',
    },
    'currency-converter.html': {
        'calc_id': 'currency',
        'func_name': 'convertCurrency',
        'func_pattern': r'function convertCurrency\(\)',
        'extra_funcs': ['swapCurrencies', 'updateExchangeRate'],
    },
    'lease-buy-calculator.html': {
        'calc_id': 'lease',
        'func_name': 'calculateLeaseBuy',
        'func_pattern': r'function calculateLeaseBuy\(\)',
    },
    'canadian-tax-calculator.html': {
        'calc_id': 'tax',
        'func_name': 'calculateTax',
        'func_pattern': r'function calculateTax\(\)',
    },
    'rrsp-refund-calculator.html': {
        'calc_id': 'rrsp',
        'func_name': 'calculateRRSP',
        'func_pattern': r'function calculateRRSP\(\)',
    },
}

def extract_function_from_index(index_content, func_name):
    """Extract a specific function from index.html"""
    # Find the function definition
    pattern = rf'function {func_name}\([^)]*\)\s*{{'
    match = re.search(pattern, index_content)
    if not match:
        print(f"Warning: Could not find function {func_name}")
        return None
    
    start = match.start()
    
    # Find the matching closing brace
    brace_count = 0
    in_function = False
    end = start
    
    for i in range(start, len(index_content)):
        char = index_content[i]
        if char == '{':
            brace_count += 1
            in_function = True
        elif char == '}':
            brace_count -= 1
            if in_function and brace_count == 0:
                end = i + 1
                break
    
    return index_content[start:end]

def extract_shared_utilities(index_content):
    """Extract shared utility functions from index.html"""
    utilities = []
    
    # Extract formatting functions
    utility_patterns = [
        r'const fmt = \(n, decimals = 0\) => \{[^}]+\};',
        r'const fmtFull = \([^)]*\) => [^;]+;',
        r'const fmtPct = \([^)]*\) => [^;]+;',
        r'const fmtNum = \([^)]*\) => [^;]+;',
    ]
    
    for pattern in utility_patterns:
        match = re.search(pattern, index_content, re.MULTILINE | re.DOTALL)
        if match:
            utilities.append(match.group(0))
    
    # Extract svgDonut function
    donut_match = re.search(
        r'function svgDonut\([^)]*\)\s*\{.*?(?=\n\s*(?:function|const|//\s*═|$))',
        index_content,
        re.MULTILINE | re.DOTALL
    )
    if donut_match:
        utilities.append(donut_match.group(0))
    
    # Extract generatePDFReport and other utility functions
    pdf_funcs = ['generatePDFReport', 'copyResults', 'shareCalculator']
    for func in pdf_funcs:
        func_code = extract_function_from_index(index_content, func)
        if func_code:
            utilities.append(func_code)
    
    return '\n\n    '.join(utilities)

def fix_calculator_page(filename, calc_info, index_content, shared_utils):
    """Fix a single calculator page"""
    print(f"Fixing {filename}...")
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the bloated script block (starts with "console.log('FiggyBank v6.0")
    script_start = content.find("    <script>\n    console.log('FiggyBank v6.0")
    if script_start == -1:
        print(f"  Warning: Could not find script block in {filename}")
        return False
    
    # Find the end of this script block (before the final initialization script)
    # Look for the closing </script> before the DOMContentLoaded script
    script_end_pattern = r'</script>\s+<script>\s+// Initialize calculator on page load'
    script_end_match = re.search(script_end_pattern, content[script_start:])
    if not script_end_match:
        print(f"  Warning: Could not find script end in {filename}")
        return False
    
    script_end = script_start + script_end_match.start() + len('</script>')
    
    # Extract the main calculator function
    main_func = extract_function_from_index(index_content, calc_info['func_name'])
    if not main_func:
        print(f"  Error: Could not extract {calc_info['func_name']}")
        return False
    
    # Extract extra functions if specified
    extra_funcs = []
    if 'extra_funcs' in calc_info:
        for extra_func_name in calc_info['extra_funcs']:
            extra_func = extract_function_from_index(index_content, extra_func_name)
            if extra_func:
                extra_funcs.append(extra_func)
    
    # Build the new minimal script
    new_script = f"""    <script>
    console.log('FiggyBank calculator loaded: {calc_info['calc_id']}');

    // ═══ SHARED UTILITY FUNCTIONS ═══
    {shared_utils}

    // ═══ DARK MODE TOGGLE ═══
    function toggleDark() {{
      document.documentElement.classList.toggle('dark');
      localStorage.setItem('theme', document.documentElement.classList.contains('dark') ? 'dark' : 'light');
    }}
    if (localStorage.getItem('theme') === 'dark' || (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {{
      document.documentElement.classList.add('dark');
    }}

    // ═══ CALCULATOR FUNCTION ═══
    {main_func}
"""
    
    # Add extra functions
    if extra_funcs:
        new_script += "\n    // ═══ ADDITIONAL FUNCTIONS ═══\n"
        new_script += "\n\n    ".join(extra_funcs)
    
    new_script += "\n  </script>"
    
    # Replace the script block
    new_content = content[:script_start] + new_script + content[script_end:]
    
    # Write the fixed content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✓ Fixed {filename}")
    return True

def main():
    """Main function to fix all calculator pages"""
    # Read the working index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    print("Extracting shared utilities from index.html...")
    shared_utils = extract_shared_utilities(index_content)
    
    print(f"\nFound {len(CALCULATOR_MAP)} calculator pages to fix\n")
    
    fixed_count = 0
    for filename, calc_info in CALCULATOR_MAP.items():
        if os.path.exists(filename):
            if fix_calculator_page(filename, calc_info, index_content, shared_utils):
                fixed_count += 1
        else:
            print(f"Warning: {filename} not found")
    
    print(f"\n{'='*60}")
    print(f"Fixed {fixed_count} out of {len(CALCULATOR_MAP)} calculator pages")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
