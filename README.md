# ML Loop Unrolling

Using ML to predict **how much** loop unrolling speeds up (or slows down) code.

## How it works

1. Compile C programs to LLVM IR
2. Extract loop features (instruction counts, trip count, etc.)
3. Benchmark with/without `-funroll-loops`
4. Train regression model to predict actual speedup
5. Use predictions to rank loops and decide what to optimize

## Setup

```bash
# Install LLVM
sudo apt install clang llvm

# Install Python deps
pip install -r requirements.txt

# Verify
python verify_setup.py
```

## Usage

```bash
# Collect dataset
python3 src/collect_dataset.py --runs 10

# Analyze data
python3 scripts/analyze_predictions.py

# Train models (opens notebook)
jupyter notebook notebooks/04_regression_model.ipynb

# Predict on new program
python3 src/predict.py benchmarks/small_loop.c
```

## Features

Extracts 14 base features + engineered ratios:
- Instruction counts (loads, stores, branches, arithmetic)
- Trip count (log scale)
- Memory/compute intensity ratios
- Control flow complexity

## Benchmarks

28 C programs → 84 loops:
- **11 basic patterns** - small/large loops, nested, branches
- **7 PolyBench kernels** - matrix multiply, stencils, graph algorithms  
- **10 generated** - string ops, dot product, histogram, etc.

Speedup range: 0.84x (unrolling hurts) to 1.37x (big win)

See `RESULTS.md` for analysis.

## Results

**Before**: Binary classification got 92.3% accuracy but baseline was 88.7% (almost useless)

**After**: Regression predicts actual speedup
- 84 loops, balanced dataset (38% beneficial vs 62%)
- Random Forest MAE: ~0.05x (avg prediction error)
- Clear patterns: stencils benefit, branches hurt

See `RESULTS.md` for full analysis.

## LLVM Integration

Comparison tools in `src/compare_decisions.py` and basic LLVM pass skeleton in `llvm-pass/` (TODO: integrate trained model).

## TODO

- Integrate trained model into LLVM pass
- Multi-class: predict unroll factor (2x, 4x, 8x) not just speedup
- More data from SPEC/LLVM test suite (target 500+ loops)
- Better features (instruction mix percentages, stride patterns)

## License

MIT
