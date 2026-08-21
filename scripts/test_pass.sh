#!/bin/bash
# Test the LLVM pass on a benchmark

if [ $# -eq 0 ]; then
    echo "Usage: $0 <benchmark.c>"
    echo "Example: $0 benchmarks/small_loop.c"
    exit 1
fi

SOURCE=$1
BASENAME=$(basename "$SOURCE" .c)

cd "$(dirname "$0")/.."

# check if pass is built
if [ ! -f "llvm-pass/build/MLUnrollPass.so" ] && [ ! -f "llvm-pass/build/MLUnrollPass.dylib" ]; then
    echo "Error: LLVM pass not built yet"
    echo "Run: cd llvm-pass && mkdir build && cd build && cmake .. && make"
    exit 1
fi

# find the pass library
PASS_LIB="llvm-pass/build/MLUnrollPass.so"
if [ ! -f "$PASS_LIB" ]; then
    PASS_LIB="llvm-pass/build/MLUnrollPass.dylib"
fi

echo "Compiling to IR..."
clang -O1 -S -emit-llvm "$SOURCE" -o "/tmp/$BASENAME.ll"

echo ""
echo "Running ML unroll pass..."
opt -load-pass-plugin="$PASS_LIB" \
    -passes="ml-unroll" \
    "/tmp/$BASENAME.ll" -o /dev/null

echo ""
echo "For comparison, LLVM's decisions:"
python src/extract_llvm_decisions.py "$SOURCE"
