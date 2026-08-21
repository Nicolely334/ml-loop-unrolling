#!/bin/bash
# Quick script to compare our features vs LLVM's decisions on all benchmarks

cd "$(dirname "$0")/.."

echo "Comparing ML features vs LLVM decisions..."
echo ""

python src/compare_decisions.py --benchmarks benchmarks/

echo ""
echo "Done. See output above for comparison."
