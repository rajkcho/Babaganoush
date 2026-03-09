#!/bin/bash
# Master test runner - runs all validation tests

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                              ║"
echo "║              🧪 FIGGYBANK CALCULATOR PAGES - FULL TEST SUITE 🧪              ║"
echo "║                                                                              ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

FAILED=0

# Test 1: Comprehensive HTML/Meta/Schema/JS/Links Tests
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "TEST 1: Comprehensive Page Validation"
echo "═══════════════════════════════════════════════════════════════════════════════"
python3 comprehensive_test.py
if [ $? -ne 0 ]; then
    FAILED=$((FAILED + 1))
fi
echo ""

# Test 2: SPA Compatibility
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "TEST 2: SPA Compatibility & Consistency"
echo "═══════════════════════════════════════════════════════════════════════════════"
python3 test_spa_compatibility.py
if [ $? -ne 0 ]; then
    FAILED=$((FAILED + 1))
fi
echo ""

# Test 3: File existence check
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "TEST 3: File Existence & Sizes"
echo "═══════════════════════════════════════════════════════════════════════════════"

calc_count=$(ls *-calculator.html currency-converter.html 2>/dev/null | wc -l)
if [ $calc_count -eq 23 ]; then
    echo "✅ All 23 calculator pages present"
else
    echo "❌ Expected 23 calculator pages, found $calc_count"
    FAILED=$((FAILED + 1))
fi

# Check file sizes (should be 300KB+)
small_files=0
for file in *-calculator.html currency-converter.html; do
    if [ -f "$file" ]; then
        size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
        if [ $size -lt 300000 ]; then
            echo "⚠️  $file is suspiciously small ($size bytes)"
            small_files=$((small_files + 1))
        fi
    fi
done

if [ $small_files -eq 0 ]; then
    echo "✅ All calculator pages are proper size (300KB+)"
else
    echo "❌ $small_files files are too small"
    FAILED=$((FAILED + 1))
fi

# Check for required files
if [ -f "sitemap.xml" ]; then
    echo "✅ sitemap.xml exists"
else
    echo "❌ sitemap.xml missing"
    FAILED=$((FAILED + 1))
fi

if [ -f "index.html" ]; then
    echo "✅ index.html (SPA) exists"
else
    echo "❌ index.html missing!"
    FAILED=$((FAILED + 1))
fi

echo ""

# Test 4: Git status
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "TEST 4: Git Repository Status"
echo "═══════════════════════════════════════════════════════════════════════════════"

# Check if we're in a git repo
if [ -d ".git" ]; then
    # Check for uncommitted changes to calculator pages
    uncommitted=$(git status --short | grep "calculator.html" | wc -l)
    if [ $uncommitted -gt 0 ]; then
        echo "⚠️  $uncommitted calculator pages have uncommitted changes:"
        git status --short | grep "calculator.html"
        echo ""
        echo "   Run: git add *-calculator.html currency-converter.html && git commit"
    else
        echo "✅ All calculator pages committed to git"
    fi
    
    # Check current branch
    branch=$(git branch --show-current)
    echo "📍 Current branch: $branch"
    
    # Check last commit
    echo "📝 Last commit:"
    git log -1 --oneline
else
    echo "⚠️  Not in a git repository"
fi

echo ""

# Final Summary
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                            TEST SUMMARY                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "🎉 ✅ ALL TESTS PASSED!"
    echo ""
    echo "   Your FiggyBank calculator pages are ready to deploy!"
    echo ""
    echo "   Next steps:"
    echo "   1. Review the changes: git diff"
    echo "   2. Commit any remaining changes: git add . && git commit -m 'Fix minor issues'"
    echo "   3. Push to GitHub: git push origin main"
    echo "   4. Verify deployment at https://figgybank.ca/"
    echo "   5. Submit sitemap to Google Search Console"
    echo ""
    exit 0
else
    echo "❌ $FAILED TEST(S) FAILED"
    echo ""
    echo "   Please fix the issues above before deploying."
    echo ""
    exit 1
fi
