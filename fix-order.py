#!/usr/bin/env python3
"""Move utility functions (fmt, fmtFull, svgDonut, svgWaterfall) before new calculator functions"""

with open('index.html', 'r') as f:
    lines = f.readlines()

# Find the utility block: from "const fmt = " to end of svgWaterfall (line before "// ── Page Navigation")
util_start = None
util_end = None
for i, line in enumerate(lines):
    if line.strip().startswith('const fmt = (n, decimals = 0)'):
        util_start = i
    if util_start and '// ── Page Navigation' in line:
        util_end = i  # exclusive - this line stays
        break

print(f"Utility block: lines {util_start+1}-{util_end}")

# Extract utility block
util_block = lines[util_start:util_end]

# Find insertion point: right before "// ── Capital Gains Tax Calculator"
insert_at = None
for i, line in enumerate(lines):
    if '// ── Capital Gains Tax Calculator' in line:
        insert_at = i
        break

print(f"Insert before line {insert_at+1}")

# Build new file: remove utility block from old position, insert before calculators
new_lines = []
for i, line in enumerate(lines):
    if i == insert_at:
        new_lines.append('\n    // ═══ UTILITY FUNCTIONS (moved before calculators) ═══\n')
        new_lines.extend(util_block)
        new_lines.append('\n')
    if util_start <= i < util_end:
        continue  # skip old position
    new_lines.append(line)

with open('index.html', 'w') as f:
    f.writelines(new_lines)

print(f"Done! {len(new_lines)} lines")
