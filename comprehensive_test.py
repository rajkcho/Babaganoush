#!/usr/bin/env python3
"""
Comprehensive testing suite for FiggyBank calculator pages
Tests HTML, JavaScript, schema markup, links, and more
"""

import os
import re
import json
from collections import defaultdict
from html.parser import HTMLParser

class HTMLValidator(HTMLParser):
    """Basic HTML validation"""
    def __init__(self):
        super().__init__()
        self.errors = []
        self.tags = []
        
    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        
    def handle_endtag(self, tag):
        if not self.tags:
            self.errors.append(f"Closing tag </{tag}> with no opening tag")
        elif self.tags[-1] != tag:
            # Check if it's a self-closing tag
            if tag not in ['img', 'br', 'hr', 'input', 'meta', 'link']:
                self.errors.append(f"Tag mismatch: expected </{self.tags[-1]}>, got </{tag}>")
        else:
            self.tags.pop()

def test_html_structure(filepath):
    """Test 1: HTML Structure Validation"""
    errors = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for basic structure
    if not content.startswith('<!DOCTYPE html>'):
        errors.append("Missing or incorrect DOCTYPE")
    
    if '<html' not in content or '</html>' not in content:
        errors.append("Missing <html> tags")
    
    if '<head>' not in content or '</head>' not in content:
        errors.append("Missing <head> section")
    
    if '<body>' not in content or '</body>' not in content:
        errors.append("Missing <body> section")
    
    # Check for unclosed tags (basic)
    open_tags = len(re.findall(r'<(div|section|nav|header|footer|main|article)\b', content))
    close_tags = len(re.findall(r'</(div|section|nav|header|footer|main|article)>', content))
    
    if abs(open_tags - close_tags) > 5:  # Allow small margin
        errors.append(f"Possible unclosed tags: {open_tags} opening, {close_tags} closing")
    
    return errors

def test_meta_tags(filepath):
    """Test 2: Meta Tags Validation"""
    errors = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_meta = {
        '<title>': 'title tag',
        'name="description"': 'meta description',
        'name="keywords"': 'meta keywords',
        'property="og:title"': 'Open Graph title',
        'property="og:description"': 'Open Graph description',
        'property="og:url"': 'Open Graph URL',
        'property="og:image"': 'Open Graph image',
        'name="twitter:card"': 'Twitter card',
        'rel="canonical"': 'canonical URL',
    }
    
    for tag, name in required_meta.items():
        if tag not in content:
            errors.append(f"Missing {name}")
    
    # Check for unique title
    title_match = re.search(r'<title>([^<]+)</title>', content)
    if title_match:
        title = title_match.group(1)
        if 'FiggyBank' not in title:
            errors.append("Title doesn't include 'FiggyBank'")
        if len(title) < 30 or len(title) > 70:
            errors.append(f"Title length ({len(title)} chars) not optimal (30-70)")
    
    return errors

def test_schema_markup(filepath):
    """Test 3: JSON-LD Schema Validation"""
    errors = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract all JSON-LD blocks
    json_ld_blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    
    if len(json_ld_blocks) < 2:
        errors.append(f"Expected at least 2 schema blocks, found {len(json_ld_blocks)}")
    
    required_types = ['WebApplication', 'FAQPage', 'BreadcrumbList']
    found_types = []
    
    for block in json_ld_blocks:
        try:
            data = json.loads(block.strip())
            if '@type' in data:
                found_types.append(data['@type'])
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON-LD: {str(e)[:100]}")
    
    for req_type in required_types:
        if req_type not in found_types:
            errors.append(f"Missing schema type: {req_type}")
    
    return errors

def test_javascript(filepath):
    """Test 4: JavaScript Presence and Basic Validation"""
    errors = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for main calculator functions
    calc_functions = [
        'calculateMortgage', 'calculateDCF', 'calculateTax', 
        'calculateRetirement', 'calculateCompound', 'toggleTheme'
    ]
    
    found_any_calc = False
    for func in calc_functions:
        if f'function {func}' in content:
            found_any_calc = True
            break
    
    if not found_any_calc:
        errors.append("No calculator functions found in JavaScript")
    
    # Check for DOMContentLoaded initialization
    if 'DOMContentLoaded' not in content:
        errors.append("Missing DOMContentLoaded event listener")
    
    # Check for common JS errors
    if 'console.log("No scripts found")' in content:
        errors.append("Placeholder script still present - actual scripts not loaded")
    
    # Basic syntax checks
    open_braces = content.count('{')
    close_braces = content.count('}')
    if abs(open_braces - close_braces) > 10:
        errors.append(f"Mismatched braces: {open_braces} open, {close_braces} close")
    
    return errors

def test_internal_links(filepath, all_pages):
    """Test 5: Internal Link Validation"""
    errors = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract all internal links
    internal_links = re.findall(r'href="(/[^"#]+\.html)"', content)
    
    for link in internal_links:
        # Remove leading /
        link_file = link[1:] if link.startswith('/') else link
        full_path = f'/home/openclaw/.openclaw/workspace/figgybank/{link_file}'
        
        if not os.path.exists(full_path) and link_file not in all_pages:
            errors.append(f"Broken internal link: {link}")
    
    return errors

def test_css_loading(filepath):
    """Test 6: CSS Presence"""
    errors = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for style tag
    if '<style>' not in content:
        errors.append("Missing <style> tag")
    
    # Check for common CSS variables
    css_vars = ['--fg-purple', '--fg-coral', '--fg-cream', '--bg-primary']
    style_section = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    
    if style_section:
        styles = style_section.group(1)
        for var in css_vars:
            if var not in styles:
                errors.append(f"Missing CSS variable: {var}")
    
    # Check for responsive design
    if '@media' not in content:
        errors.append("No media queries found - possibly not responsive")
    
    return errors

def test_calculator_specific(filepath):
    """Test 7: Calculator-Specific Elements"""
    errors = []
    filename = os.path.basename(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for calculator HTML structure
    if 'calc-container' not in content and 'page' not in content:
        errors.append("Missing calculator container structure")
    
    # Check for input fields
    if '<input' not in content and '<select' not in content:
        errors.append("No input fields found")
    
    # Check for results area
    if 'calc-results' not in content and 'results' not in content:
        errors.append("No results area found")
    
    # Check for related calculators section
    if 'related-calculators' not in content:
        errors.append("Missing related calculators section")
    
    # Check for SEO content section
    if 'seo-content' not in content:
        errors.append("Missing SEO content section")
    
    return errors

def test_unique_content(all_files):
    """Test 8: Ensure Unique Titles and Descriptions"""
    errors = []
    titles = {}
    descriptions = {}
    
    for filepath in all_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        filename = os.path.basename(filepath)
        
        # Extract title
        title_match = re.search(r'<title>([^<]+)</title>', content)
        if title_match:
            title = title_match.group(1)
            if title in titles:
                errors.append(f"Duplicate title in {filename} and {titles[title]}: {title}")
            else:
                titles[title] = filename
        
        # Extract description
        desc_match = re.search(r'name="description" content="([^"]+)"', content)
        if desc_match:
            desc = desc_match.group(1)
            if desc in descriptions:
                errors.append(f"Duplicate description in {filename} and {descriptions[desc]}")
            else:
                descriptions[desc] = filename
    
    return errors

def test_sitemap():
    """Test 9: Sitemap Validation"""
    errors = []
    sitemap_path = '/home/openclaw/.openclaw/workspace/figgybank/sitemap.xml'
    
    if not os.path.exists(sitemap_path):
        return ["sitemap.xml not found"]
    
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for XML declaration
    if not content.startswith('<?xml'):
        errors.append("Missing XML declaration")
    
    # Check for required elements
    if '<urlset' not in content:
        errors.append("Missing <urlset> element")
    
    # Count URLs
    url_count = len(re.findall(r'<url>', content))
    if url_count < 23:
        errors.append(f"Expected at least 23 calculator URLs in sitemap, found {url_count}")
    
    # Check for calculator URLs
    calc_files = [f for f in os.listdir('/home/openclaw/.openclaw/workspace/figgybank') 
                  if f.endswith('-calculator.html') or f == 'currency-converter.html']
    
    missing_from_sitemap = []
    for calc in calc_files:
        if calc not in content:
            missing_from_sitemap.append(calc)
    
    if missing_from_sitemap:
        errors.append(f"Missing from sitemap: {', '.join(missing_from_sitemap[:5])}")
    
    return errors

def test_mobile_viewport(filepath):
    """Test 10: Mobile Responsiveness Meta Tag"""
    errors = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'name="viewport"' not in content:
        errors.append("Missing viewport meta tag")
    elif 'width=device-width' not in content:
        errors.append("Viewport tag doesn't set width=device-width")
    
    return errors

def run_all_tests():
    """Run comprehensive test suite"""
    os.chdir('/home/openclaw/.openclaw/workspace/figgybank')
    
    # Get all calculator pages
    calc_pages = [f for f in os.listdir('.') 
                  if (f.endswith('-calculator.html') or f == 'currency-converter.html')]
    calc_pages.sort()
    
    print("🧪 COMPREHENSIVE TESTING SUITE FOR FIGGYBANK CALCULATOR PAGES")
    print("=" * 80)
    print(f"\nTesting {len(calc_pages)} calculator pages...\n")
    
    all_errors = defaultdict(list)
    test_results = {}
    
    # Test each page
    for i, page in enumerate(calc_pages, 1):
        filepath = f'./{page}'
        page_errors = {}
        
        print(f"[{i}/{len(calc_pages)}] Testing: {page}")
        
        # Run all tests
        tests = [
            ("HTML Structure", test_html_structure),
            ("Meta Tags", test_meta_tags),
            ("Schema Markup", test_schema_markup),
            ("JavaScript", test_javascript),
            ("Internal Links", lambda f: test_internal_links(f, calc_pages)),
            ("CSS Loading", test_css_loading),
            ("Calculator Elements", test_calculator_specific),
            ("Mobile Viewport", test_mobile_viewport),
        ]
        
        for test_name, test_func in tests:
            errors = test_func(filepath)
            if errors:
                page_errors[test_name] = errors
                all_errors[page] += errors
        
        if page_errors:
            print(f"  ❌ {len(sum(page_errors.values(), []))} issues found")
            for test_name, errors in page_errors.items():
                for error in errors:
                    print(f"     • {test_name}: {error}")
        else:
            print(f"  ✅ All tests passed")
        
        test_results[page] = page_errors
    
    print("\n" + "=" * 80)
    print("CROSS-PAGE TESTS")
    print("=" * 80 + "\n")
    
    # Test unique content across all pages
    print("[9] Testing: Unique Titles & Descriptions")
    unique_errors = test_unique_content([f'./{p}' for p in calc_pages])
    if unique_errors:
        print(f"  ❌ {len(unique_errors)} duplicate content issues")
        for error in unique_errors:
            print(f"     • {error}")
    else:
        print(f"  ✅ All titles and descriptions unique")
    
    # Test sitemap
    print("\n[10] Testing: Sitemap Validation")
    sitemap_errors = test_sitemap()
    if sitemap_errors:
        print(f"  ❌ {len(sitemap_errors)} sitemap issues")
        for error in sitemap_errors:
            print(f"     • {error}")
    else:
        print(f"  ✅ Sitemap valid")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80 + "\n")
    
    total_errors = sum(len(errs) for errs in all_errors.values()) + len(unique_errors) + len(sitemap_errors)
    pages_with_errors = len([p for p in test_results if test_results[p]])
    pages_passed = len(calc_pages) - pages_with_errors
    
    print(f"📊 Pages tested: {len(calc_pages)}")
    print(f"✅ Pages passed: {pages_passed}")
    print(f"❌ Pages with issues: {pages_with_errors}")
    print(f"⚠️  Total issues found: {total_errors}")
    
    if total_errors == 0:
        print("\n" + "=" * 80)
        print("🎉 ALL TESTS PASSED! Ready to deploy.")
        print("=" * 80)
        return True
    else:
        print("\n" + "=" * 80)
        print("⚠️  ISSUES FOUND - Review and fix before deploying")
        print("=" * 80)
        
        # Show top issues
        print("\n🔍 Most Common Issues:")
        issue_types = defaultdict(int)
        for page_errors in test_results.values():
            for test_name in page_errors:
                issue_types[test_name] += 1
        
        for test_name, count in sorted(issue_types.items(), key=lambda x: -x[1]):
            print(f"   • {test_name}: {count} pages affected")
        
        return False

if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)
