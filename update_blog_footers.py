#!/usr/bin/env python3
"""Update footer links in all blog post HTML files"""

import os
import glob

blog_dir = 'blog'

# Old footer links section
old_footer = '''<div style="display:flex;gap:2rem;justify-content:center;flex-wrap:wrap;margin-bottom:2.5rem;">
        <a href="/" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.85rem;transition:color 0.3s;">Calculators</a>
        <a href="/glossary.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.85rem;transition:color 0.3s;">Glossary</a>
        <a href="/quiz.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.85rem;transition:color 0.3s;">Financial Quiz</a>
        <a href="/blog/" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.85rem;transition:color 0.3s;">Blog</a>
      </div>'''

# New footer links section with About, Privacy, Contact
new_footer = '''<div style="display:flex;gap:2rem;justify-content:center;flex-wrap:wrap;margin-bottom:2.5rem;">
        <a href="/" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.85rem;transition:color 0.3s;">Calculators</a>
        <a href="/about.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.85rem;transition:color 0.3s;">About</a>
        <a href="/privacy.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.85rem;transition:color 0.3s;">Privacy</a>
        <a href="/contact.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.85rem;transition:color 0.3s;">Contact</a>
        <a href="/glossary.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.85rem;transition:color 0.3s;">Glossary</a>
        <a href="/blog/" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.85rem;transition:color 0.3s;">Blog</a>
      </div>'''

# Get all HTML files in blog directory
blog_files = glob.glob(os.path.join(blog_dir, '*.html'))

updated_count = 0
for blog_file in blog_files:
    # Read file
    with open(blog_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace footer links
    if old_footer in content:
        new_content = content.replace(old_footer, new_footer)
        
        # Write back
        with open(blog_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        updated_count += 1
        print(f"✅ Updated: {os.path.basename(blog_file)}")
    else:
        print(f"⚠️  Skipped: {os.path.basename(blog_file)} (footer not found or already updated)")

print(f"\n✨ Updated {updated_count} blog post(s)")
