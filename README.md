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

## TODO

- [ ] Add more benchmarks
- [ ] Try more ML models (XGBoost, etc)
- [ ] Extract LLVM's actual unrolling decisions
- [ ] Handle multi-file programs

## License

MIT
