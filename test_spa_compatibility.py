#!/usr/bin/env python3
"""
Test that the original SPA (index.html) still works correctly
"""

import os
import re

def test_spa_unchanged():
    """Verify index.html wasn't accidentally modified"""
    errors = []
    
    filepath = '/home/openclaw/.openclaw/workspace/figgybank/index.html'
    
    if not os.path.exists(filepath):
        return ["index.html not found!"]
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check SPA structure
    if 'id="page-home"' not in content:
        errors.append("Missing home page div")
    
    if 'id="page-mortgage"' not in content:
        errors.append("Missing mortgage calculator page div")
    
    if 'id="page-valuation"' not in content:
        errors.append("Missing valuation calculator page div")
    
    # Check for showPage function
    if 'function showPage(pageId)' not in content:
        errors.append("Missing showPage() function")
    
    # Check hash routing
    if 'window.location.hash' not in content:
        errors.append("Missing hash-based routing")
    
    # Count calculator pages in SPA
    page_divs = len(re.findall(r'id="page-\w+"', content))
    if page_divs < 20:
        errors.append(f"Expected 20+ calculator pages in SPA, found {page_divs}")
    
    return errors

def test_no_broken_references():
    """Check that individual pages don't reference non-existent files"""
    errors = []
    
    calc_pages = [f for f in os.listdir('/home/openclaw/.openclaw/workspace/figgybank') 
                  if f.endswith('-calculator.html') or f == 'currency-converter.html']
    
    for page in calc_pages:
        with open(f'/home/openclaw/.openclaw/workspace/figgybank/{page}', 'r') as f:
            content = f.read()
        
        # Check that pages don't reference a non-existent shared.js or shared.css
        if 'src="shared.js"' in content or 'src="/shared.js"' in content:
            errors.append(f"{page} references non-existent shared.js")
        
        if 'href="shared.css"' in content or 'href="/shared.css"' in content:
            errors.append(f"{page} references non-existent shared.css")
        
        # Check that styles are embedded
        if '<style>' not in content:
            errors.append(f"{page} missing embedded styles")
        
        # Check that scripts are embedded
        if '<script>' not in content or 'function' not in content:
            errors.append(f"{page} missing embedded scripts")
    
    return errors

def test_navigation_consistency():
    """Check that navigation is consistent across all pages"""
    errors = []
    
    calc_pages = [f for f in os.listdir('/home/openclaw/.openclaw/workspace/figgybank') 
                  if f.endswith('-calculator.html') or f == 'currency-converter.html']
    
    # Check that all pages have the same nav structure
    nav_links = []
    
    for page in calc_pages[:3]:  # Sample first 3 pages
        with open(f'/home/openclaw/.openclaw/workspace/figgybank/{page}', 'r') as f:
            content = f.read()
        
        # Extract nav structure
        nav_match = re.search(r'<nav class="nav-bar"(.*?)</nav>', content, re.DOTALL)
        if nav_match:
            nav = nav_match.group(1)
            
            # Check for key navigation elements
            if 'Calculators' not in nav:
                errors.append(f"{page} missing Calculators dropdown")
            
            if 'Tools' not in nav:
                errors.append(f"{page} missing Tools dropdown")
            
            if 'Blog' not in nav:
                errors.append(f"{page} missing Blog link")
            
            if 'theme-toggle' not in content:
                errors.append(f"{page} missing dark mode toggle")
    
    return errors

def run_all_compatibility_tests():
    """Run all compatibility tests"""
    print("🔄 TESTING SPA COMPATIBILITY & CONSISTENCY")
    print("=" * 80)
    
    all_tests = [
        ("Original SPA Unchanged", test_spa_unchanged),
        ("No Broken References", test_no_broken_references),
        ("Navigation Consistency", test_navigation_consistency),
    ]
    
    total_errors = 0
    
    for test_name, test_func in all_tests:
        print(f"\n[{test_name}]")
        errors = test_func()
        
        if errors:
            print(f"  ❌ {len(errors)} issues found:")
            for error in errors:
                print(f"     • {error}")
            total_errors += len(errors)
        else:
            print(f"  ✅ Passed")
    
    print("\n" + "=" * 80)
    if total_errors == 0:
        print("✅ ALL COMPATIBILITY TESTS PASSED")
        return True
    else:
        print(f"⚠️  {total_errors} ISSUES FOUND")
        return False

if __name__ == '__main__':
    success = run_all_compatibility_tests()
    exit(0 if success else 1)
