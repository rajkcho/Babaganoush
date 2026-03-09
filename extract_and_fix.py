#!/usr/bin/env python3
"""
Extract utilities and specific calculator functions from index.html
and rebuild the broken calculator pages with minimal JS.
"""

import re
import os

# Map calculator pages to their primary functions
CALCULATORS = {
    'business-valuation-calculator.html': {
        'id': 'valuation',
        'functions': ['calculateDCF', 'calculateMultiples', 'calculateAsset', 'setIndustryPreset'],
    },
    'canadian-tax-calculator.html': {
        'id': 'tax',
        'functions': ['calculateTax', 'calcBracketTax', 'getMarginalRate', 'getProvBrackets', 'getProvBasic', 'getProvDTCRate'],
    },
    'capital-gains-calculator.html': {
        'id': 'capgains',
        'functions': ['calculateCapGains'],
    },
    'comparison-calculator.html': {
        'id': 'compare',
        'functions': ['calculateComparison'],
    },
    'compound-interest-calculator.html': {
        'id': 'compound',
        'functions': ['calculateCompound'],
    },
    'cpp-oas-calculator.html': {
        'id': 'cpp',
        'functions': ['calculateCPP'],
    },
    'currency-converter.html': {
        'id': 'currency',
        'functions': ['convertCurrency', 'swapCurrencies', 'updateExchangeRate'],
    },
    'debt-payoff-calculator.html': {
        'id': 'debt',
        'functions': ['calculateDebt'],
    },
    'fhsa-calculator.html': {
        'id': 'fhsa',
        'functions': ['calculateFHSA'],
    },
    'gic-ladder-calculator.html': {
        'id': 'gic',
        'functions': ['calculateGIC'],
    },
    'income-tax-calculator.html': {
        'id': 'incometax',
        'functions': ['calculateIncomeTax', 'calcBracketTax', 'getMarginalRate', 'getProvBrackets', 'getProvBasic', 'getProvDTCRate'],
    },
    'investment-returns-calculator.html': {
        'id': 'investment',
        'functions': ['calculateCAGR', 'calculateDCA', 'calculateRetirement'],
    },
    'lease-buy-calculator.html': {
        'id': 'lease',
        'functions': ['calculateLeaseBuy'],
    },
    'merger-acquisition-calculator.html': {
        'id': 'merger',
        'functions': ['calculateMA'],
    },
    'mortgage-calculator.html': {
        'id': 'mortgage',
        'functions': ['calculateMortgage'],
    },
    'net-worth-calculator.html': {
        'id': 'networth',
        'functions': ['calculateNetWorth', 'loadNetWorthSnapshots', 'saveNetWorthSnapshot', 'deleteSnapshot'],
    },
    'rent-buy-calculator.html': {
        'id': 'rentbuy',
        'functions': ['calculateRentBuy'],
    },
    'resp-calculator.html': {
        'id': 'resp',
        'functions': ['calculateRESP'],
    },
    'rrsp-refund-calculator.html': {
        'id': 'rrsp',
        'functions': ['calculateRRSP'],
    },
    'rrsp-tfsa-calculator.html': {
        'id': 'retirement',
        'functions': ['calculateRRSP', 'calculateTFSA'],
    },
    'salary-compensation-calculator.html': {
        'id': 'salary',
        'functions': ['calculateSalary'],
    },
    'startup-runway-calculator.html': {
        'id': 'runway',
        'functions': ['calculateRunway', 'addHireRow'],
    },
    'tfsa-contribution-calculator.html': {
        'id': 'tfsa',
        'functions': ['calculateTFSA'],
    },
}

def extract_function_smart(content, func_name):
    """
    Extract a function definition from JavaScript code.
    Handles both 'function name()' and 'const name = ()' styles.
    Handles both indented (4 spaces) and non-indented functions.
    """
    # Try different function definition patterns
    patterns = [
        # Standard function declaration (with 4-space indent)
        rf'\n    function {re.escape(func_name)}\s*\([^)]*\)\s*{{',
        # Standard function declaration (no indent)
        rf'\nfunction {re.escape(func_name)}\s*\([^)]*\)\s*{{',
        # Const arrow function (with indent)
        rf'\n    const {re.escape(func_name)}\s*=\s*\([^)]*\)\s*=>\s*{{',
        # Const arrow function (no indent)
        rf'\nconst {re.escape(func_name)}\s*=\s*\([^)]*\)\s*=>\s*{{',
        # Var function (with indent)
        rf'\n    var {re.escape(func_name)}\s*=\s*function\s*\([^)]*\)\s*{{',
        # Var function (no indent)
        rf'\nvar {re.escape(func_name)}\s*=\s*function\s*\([^)]*\)\s*{{',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            start_pos = match.start() + 1  # Skip the leading \n
            
            # Find the matching closing brace
            brace_count = 0
            in_function = False
            pos = match.end() - 1  # Position of the opening brace
            
            for i in range(pos, len(content)):
                char = content[i]
                if char == '{':
                    brace_count += 1
                    in_function = True
                elif char == '}':
                    brace_count -= 1
                    if in_function and brace_count == 0:
                        # Include the closing brace and newline
                        end_pos = i + 1
                        return content[start_pos:end_pos]
            
            # If we didn't find a closing brace, return what we have
            print(f"Warning: Could not find closing brace for {func_name}")
            return content[start_pos:start_pos + 500] + "\n    // ... truncated ...\n    }\n"
    
    print(f"Warning: Function {func_name} not found")
    return None

def extract_shared_utilities(index_content):
    """
    Extract all shared utility functions from index.html.
    These are the formatting, charting, and helper functions used across calculators.
    """
    # Find the start of utility functions (around line 7531)
    util_start_pattern = r'\n    // ═══ UTILITY FUNCTIONS'
    util_start = re.search(util_start_pattern, index_content)
    
    if not util_start:
        print("Warning: Could not find utility functions section")
        return ""
    
    start_pos = util_start.start() + 1
    
    # Find the end (before the first calculator function)
    # Look for the Capital Gains Calculator or similar marker
    util_end_pattern = r'\n    // ═══.*?CALCULATOR.*?\n    function calculate'
    util_end = re.search(util_end_pattern, index_content[start_pos:])
    
    if util_end:
        end_pos = start_pos + util_end.start()
    else:
        # Fallback: find calculateCapGains or similar
        calc_pattern = r'\n    function calculateCapGains\('
        calc_match = re.search(calc_pattern, index_content[start_pos:])
        if calc_match:
            end_pos = start_pos + calc_match.start()
        else:
            end_pos = start_pos + 6000  # Approximate
    
    utilities = index_content[start_pos:end_pos]
    
    # Clean up trailing newlines
    utilities = utilities.rstrip() + '\n'
    
    return utilities

def build_minimal_script(calc_id, functions, index_content, shared_utils):
    """
    Build a minimal <script> block for a calculator page.
    """
    # Extract all needed calculator functions
    extracted_funcs = []
    for func_name in functions:
        func_code = extract_function_smart(index_content, func_name)
        if func_code:
            extracted_funcs.append(func_code)
        else:
            print(f"  Warning: Could not extract {func_name}")
    
    # Build the script
    script = f"""    <script>
    console.log('FiggyBank calculator loaded: {calc_id}');

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

    // ═══ CALCULATOR FUNCTIONS ═══
"""
    
    for func_code in extracted_funcs:
        script += func_code + '\n\n'
    
    # Add the initialization code
    script += f"""
    // ═══ INITIALIZATION ═══
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
  </script>"""
    
    return script

def fix_calculator_page(filename, calc_info, index_content, shared_utils):
    """
    Replace the bloated script in a calculator page with a minimal one.
    """
    print(f"Fixing {filename}...")
    
    if not os.path.exists(filename):
        print(f"  Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the script block to replace
    # The bloated script starts with "    <script>\n    console.log('FiggyBank v6.0"
    # and ends with "</script>\n</body>" (it's the last script before closing body)
    script_start_pattern = r'    <script>\s*\n\s*console\.log\([\'"]FiggyBank v6\.0'
    script_start = re.search(script_start_pattern, content)
    
    if not script_start:
        print(f"  Error: Could not find script start in {filename}")
        return False
    
    start_pos = script_start.start()
    
    # Find the end: look for </script>\n</body>\n</html>
    script_end_pattern = r'</script>\s*\n\s*</body>\s*\n\s*</html>'
    script_end = re.search(script_end_pattern, content[start_pos:])
    
    if not script_end:
        print(f"  Error: Could not find script end in {filename}")
        return False
    
    end_pos = start_pos + script_end.start() + len('</script>')
    
    # Build the new script
    new_script = build_minimal_script(
        calc_info['id'],
        calc_info['functions'],
        index_content,
        shared_utils
    )
    
    # Replace
    new_content = content[:start_pos] + new_script + content[end_pos:]
    
    # Validate: check that the new content is significantly smaller
    old_size = len(content)
    new_size = len(new_content)
    reduction = old_size - new_size
    
    if reduction > 0:
        print(f"  ✓ Reduced from {old_size:,} to {new_size:,} bytes (saved {reduction:,} bytes)")
    else:
        print(f"  Warning: Size increased from {old_size:,} to {new_size:,} bytes")
    
    # Write the fixed file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    print("="*70)
    print(" FiggyBank Calculator Fixer")
    print("="*70)
    
    # Read index.html
    print("\nReading index.html...")
    with open('index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    print(f"Loaded index.html ({len(index_content):,} bytes)")
    
    # Extract shared utilities
    print("\nExtracting shared utilities...")
    shared_utils = extract_shared_utilities(index_content)
    print(f"Extracted {len(shared_utils):,} bytes of shared utilities")
    
    # Fix each calculator
    print(f"\nFixing {len(CALCULATORS)} calculator pages...\n")
    fixed_count = 0
    failed = []
    
    for filename, calc_info in sorted(CALCULATORS.items()):
        if fix_calculator_page(filename, calc_info, index_content, shared_utils):
            fixed_count += 1
        else:
            failed.append(filename)
    
    print("\n" + "="*70)
    print(f"Results: {fixed_count}/{len(CALCULATORS)} pages fixed")
    if failed:
        print(f"Failed: {', '.join(failed)}")
    print("="*70)

if __name__ == '__main__':
    os.chdir('/home/openclaw/.openclaw/workspace/figgybank')
    main()
