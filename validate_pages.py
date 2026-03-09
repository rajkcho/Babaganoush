#!/usr/bin/env python3
"""
Quick validation of generated calculator pages
"""

import os
import re
from collections import defaultdict

def validate_page(filepath):
    """Validate a single calculator page"""
    errors = []
    warnings = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check title tag
    if not re.search(r'<title>[^<]{30,70}</title>', content):
        errors.append("Title tag missing or not 30-70 chars")
    
    # Check meta description
    if not re.search(r'<meta name="description" content="[^"]{120,160}"', content):
        warnings.append("Meta description not 120-160 chars (may be OK)")
    
    # Check canonical
    if '<link rel="canonical"' not in content:
        errors.append("Missing canonical URL")
    
    # Check Open Graph
    if 'property="og:title"' not in content:
        errors.append("Missing Open Graph tags")
    
    # Check schema markup
    if '"@type": "FAQPage"' not in content:
        warnings.append("Missing FAQ schema")
    
    if '"@type": "WebApplication"' not in content:
        errors.append("Missing WebApplication schema")
    
    # Check for JavaScript
    if 'function calculate' not in content:
        errors.append("Missing calculator JavaScript functions")
    
    # Check for SEO content
    if '<div class="seo-content"' not in content:
        warnings.append("Missing SEO content section")
    
    # Check for related calculators
    if '<div class="related-calculators"' not in content:
        warnings.append("Missing related calculators section")
    
    # Check file size
    size_kb = len(content) / 1024
    if size_kb < 200:
        errors.append(f"File too small ({size_kb:.0f}KB) - likely missing JavaScript")
    elif size_kb > 600:
        warnings.append(f"File large ({size_kb:.0f}KB) - consider optimization")
    
    return errors, warnings, size_kb

def main():
    os.chdir('/home/openclaw/.openclaw/workspace/figgybank')
    
    # Get all calculator pages
    pages = [f for f in os.listdir('.') if f.endswith('-calculator.html')]
    pages.sort()
    
    print("🔍 Validating calculator pages...\n")
    print(f"{'Page':<40} {'Size':<10} {'Status'}")
    print("-" * 70)
    
    total_errors = 0
    total_warnings = 0
    
    for page in pages:
        errors, warnings, size_kb = validate_page(page)
        
        total_errors += len(errors)
        total_warnings += len(warnings)
        
        status = "✅" if not errors else "❌"
        
        print(f"{page:<40} {size_kb:>6.0f} KB   {status}")
        
        if errors:
            for err in errors:
                print(f"  ❌ {err}")
        if warnings:
            for warn in warnings:
                print(f"  ⚠️  {warn}")
    
    print()
    print("=" * 70)
    print(f"📊 Summary:")
    print(f"  Total pages: {len(pages)}")
    print(f"  Errors: {total_errors}")
    print(f"  Warnings: {total_warnings}")
    
    if total_errors == 0:
        print("\n✅ All pages validated successfully!")
    else:
        print(f"\n⚠️  {total_errors} errors found - review above")
    
    # Check sitemap
    print("\n🗺️  Checking sitemap...")
    if os.path.exists('sitemap.xml'):
        with open('sitemap.xml', 'r') as f:
            sitemap = f.read()
        
        missing = []
        for page in pages:
            if page not in sitemap:
                missing.append(page)
        
        if missing:
            print(f"  ⚠️  {len(missing)} pages missing from sitemap:")
            for p in missing:
                print(f"     - {p}")
        else:
            print(f"  ✅ All {len(pages)} pages in sitemap")
    else:
        print("  ❌ sitemap.xml not found")

if __name__ == '__main__':
    main()
