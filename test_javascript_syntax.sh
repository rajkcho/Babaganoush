#!/bin/bash
# Test JavaScript syntax in calculator pages using Node.js

echo "🔍 TESTING JAVASCRIPT SYNTAX"
echo "============================================================================"

# Check if node is available
if ! command -v node &> /dev/null; then
    echo "⚠️  Node.js not found - skipping JS syntax validation"
    echo "   (JavaScript presence already validated in Python tests)"
    exit 0
fi

# Create a temp file to extract and test JS
TEMP_JS="/tmp/test_calculator.js"

# Count files
total=0
passed=0
failed=0

for file in *-calculator.html currency-converter.html; do
    if [ ! -f "$file" ]; then
        continue
    fi
    
    ((total++))
    
    # Extract JavaScript from HTML (between <script> tags that aren't JSON-LD)
    # This is a simple extraction - won't be perfect but good enough for syntax check
    sed -n '/<script>.*function/,/<\/script>/p' "$file" | \
        grep -v "application/ld+json" | \
        sed 's/<script>//g' | \
        sed 's/<\/script>//g' > "$TEMP_JS"
    
    # Check if we got any JavaScript
    if [ ! -s "$TEMP_JS" ]; then
        echo "⚠️  $file - No JavaScript functions found"
        continue
    fi
    
    # Try to parse with Node.js
    if node -c "$TEMP_JS" 2>/dev/null; then
        ((passed++))
        echo "✅ $file - JavaScript syntax valid"
    else
        ((failed++))
        echo "❌ $file - JavaScript syntax errors detected"
        node -c "$TEMP_JS" 2>&1 | head -3 | sed 's/^/   /'
    fi
done

rm -f "$TEMP_JS"

echo ""
echo "============================================================================"
echo "📊 JavaScript Syntax Test Results:"
echo "   Total files: $total"
echo "   Passed: $passed"
echo "   Failed: $failed"

if [ $failed -eq 0 ]; then
    echo ""
    echo "✅ ALL JAVASCRIPT SYNTAX TESTS PASSED"
    exit 0
else
    echo ""
    echo "⚠️  JAVASCRIPT SYNTAX ERRORS FOUND"
    exit 1
fi
