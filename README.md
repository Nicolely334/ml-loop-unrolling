# ML Loop Unrolling

Predicting when loop unrolling helps performance using machine learning on LLVM IR features.

## How it works

1. Compile C programs to LLVM IR
2. Extract loop features (instruction counts, trip count, etc.)
3. Benchmark with/without `-funroll-loops`
4. Train ML model on the data
5. Predict whether new loops should be unrolled

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
python src/collect_dataset.py --runs 20

# Train models (opens notebook)
jupyter notebook notebooks/02_train_models.ipynb

# Predict on new program
python src/predict.py benchmarks/small_loop.c
```

## Features

Extracts 14 features per loop:
- Instruction counts (loads, stores, branches, calls, arithmetic)
- Trip count (estimated from IR)
- Memory dependencies
- Control flow (exits, phi nodes)

## Benchmarks

11 C programs with different characteristics:
- Small/large loops
- Memory vs compute-intensive
- Nested loops
- Loops with branches
- Different access patterns

See `benchmarks/README.md` for details.

## Advanced Features

### Compare Against LLVM

See what LLVM actually decides to unroll:

```bash
# single file
python src/extract_llvm_decisions.py benchmarks/small_loop.c

# compare our features vs LLVM's decisions
python src/compare_decisions.py

# or use the script
./scripts/compare_all.sh
```

### LLVM Pass (Experimental)

Custom LLVM optimization pass that uses ML heuristics:

```bash
cd llvm-pass
mkdir build && cd build
cmake .. && make

# test it
cd ../..
./scripts/test_pass.sh benchmarks/small_loop.c
```

See `llvm-pass/README.md` for details.

## TODO

- [ ] Integrate actual ML model into LLVM pass
- [ ] Make pass actually modify IR (currently just analyzes)
- [ ] Better loop matching between our detection and LLVM's
- [ ] Multi-class prediction (unroll factor: 2, 4, 8, 16)
- [ ] Try XGBoost, neural nets
- [ ] Real benchmark suites (SPEC, PolyBench)

## License

MIT
