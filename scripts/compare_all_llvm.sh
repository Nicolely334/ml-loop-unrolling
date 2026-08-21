#!/bin/bash
# Compare ML predictions vs LLVM's actual unrolling decisions for all benchmarks

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "=========================================="
echo "ML Model vs LLVM Comparison"
echo "=========================================="
echo

# Find all C files
BENCHMARKS=$(find benchmarks -name "*.c" | sort)
TOTAL=$(echo "$BENCHMARKS" | wc -l)
COUNT=0

for BENCH in $BENCHMARKS; do
    COUNT=$((COUNT + 1))
    BASENAME=$(basename "$BENCH")
    
    echo "[$COUNT/$TOTAL] $BASENAME"
    echo "------------------------------------------"
    
    python3 src/compare_decisions.py "$BENCH" 2>&1 | grep -A20 "Comparison"
    
    echo
done

echo "=========================================="
echo "Summary"
echo "=========================================="
echo "Analyzed $TOTAL benchmarks"
echo "Check individual outputs above for disagreements"
