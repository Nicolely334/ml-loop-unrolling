# LLVM Pass for ML-Based Loop Unrolling

Custom LLVM optimization pass that uses machine learning to decide when to unroll loops.

## Current Status

**Phase 1**: ✅ Feature extraction working  
**Phase 2**: ✅ Simple heuristic-based decisions  
**Phase 3**: ⏳ TODO - integrate actual ML model  
**Phase 4**: ⏳ TODO - actually apply transformations

Right now the pass analyzes loops and prints decisions but doesn't modify IR.

## Building

You need LLVM development files installed:

```bash
# Ubuntu/Debian
sudo apt install llvm-14-dev clang-14

# macOS
brew install llvm
```

Build the pass:

```bash
cd llvm-pass
mkdir build && cd build
cmake ..
make
```

This creates `MLUnrollPass.so` (or `.dylib` on macOS).

## Using the Pass

Run it with opt:

```bash
# compile to IR first
clang -O1 -S -emit-llvm ../benchmarks/small_loop.c -o small_loop.ll

# run our pass
opt -load-pass-plugin=./build/MLUnrollPass.so \
    -passes="ml-unroll" \
    small_loop.ll -o /dev/null
```

You should see output like:
```
MLUnrollPass analyzing function: main
  Loop 1: 8 instructions, 0 loads, 0 stores -> UNROLL
  Total: 1 loops, 1 marked for unrolling
```

## How It Works

1. **Feature extraction** - counts instructions, loads, stores in each loop
2. **Decision heuristic** - applies simple rules:
   - Small loops (< 20 instructions): UNROLL
   - Large loops (> 100 instructions): SKIP
   - Memory-heavy loops (> 50% mem ops): SKIP
3. **Report** - prints analysis (doesn't modify IR yet)

## TODOs

- [ ] Actually apply unroll transformation (call UnrollLoop())
- [ ] Load Python ML model predictions (via subprocess or serialized file)
- [ ] Extract trip count using ScalarEvolution
- [ ] Add more features (phi nodes, nesting depth, etc)
- [ ] Benchmark against LLVM's default heuristics
- [ ] Support configurable unroll factors (2, 4, 8, 16)

## Integration with ML Model

Options being considered:

1. **Serialized predictions** - run Python script first, save predictions to JSON, pass reads them
2. **Subprocess** - pass calls Python script with loop features, gets prediction back
3. **ONNX Runtime** - export model to ONNX, load in C++ with ONNX Runtime
4. **Heuristic approximation** - use simple rules derived from model's learned patterns

Currently using option #4 (simple heuristics based on our ML findings).

## Notes

- This is a new-style pass (PassPlugin API)
- Works with LLVM 13+
- Old-style legacy pass API is deprecated
- See LLVM docs: https://llvm.org/docs/WritingAnLLVMNewPMPass.html
