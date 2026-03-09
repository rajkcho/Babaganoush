#!/bin/bash
# Validate all 23 calculator pages

echo "========================================================================"
echo " Validating All 23 Calculator Pages"
echo "========================================================================"

FAILED=0
PASSED=0

for file in *-calculator.html; do
    echo -n "Testing $file... "
    
    # Extract JavaScript and test syntax
    awk '/<script>/{flag=1;next}/<\/script>/{flag=0}flag' "$file" > /tmp/test_calc.js
    
    if node -c /tmp/test_calc.js 2>/dev/null; then
        # Check file size is reasonable (not bloated)
        SIZE=$(wc -c < "$file")
        if [ $SIZE -lt 200000 ]; then
            echo "✓ Valid JS, ${SIZE} bytes"
            PASSED=$((PASSED + 1))
        else
            echo "✗ BLOATED (${SIZE} bytes)"
            FAILED=$((FAILED + 1))
        fi
    else
        echo "✗ SYNTAX ERROR"
        node -c /tmp/test_calc.js 2>&1 | head -3
        FAILED=$((FAILED + 1))
    fi
done

echo "========================================================================"
echo "Results: $PASSED passed, $FAILED failed"
echo "========================================================================"

rm -f /tmp/test_calc.js

exit $FAILED
