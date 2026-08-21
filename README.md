# ML-Based Loop Unrolling Prediction

Using machine learning to help compilers decide when to unroll loops.

## Goal

This project aims to predict whether loop unrolling will improve program performance based on characteristics of the loop.

## Approach

1. Collect programs from the LLVM Test Suite
2. Identify loops in LLVM IR
3. Extract features from each loop
4. Measure performance with and without loop unrolling
5. Use the performance difference to create labels
6. Train a machine learning model to predict whether unrolling will help
7. Compare the ML model against LLVM's existing optimization behavior

## Tech Stack
- Python 3.9+
- LLVM/Clang (for compilation and IR analysis)
- C/C++ (benchmark programs)
- scikit-learn (machine learning)
- pandas, numpy (data processing)
- matplotlib, seaborn (visualization)
- Jupyter (notebooks)

## Quick Start

### 1. Install Dependencies

```bash
# Install LLVM/Clang (Ubuntu/Debian)
sudo apt install -y clang llvm

# Install Python dependencies
pip install -r requirements.txt
```

See [SETUP.md](SETUP.md) for detailed installation instructions for other platforms.

### 2. Verify Setup

```bash
python verify_setup.py
```

### 3. Run the Pipeline

```bash
# Benchmark simple_loop.c
python src/compile_and_measure.py benchmarks/simple_loop.c

# Extract loop features from LLVM IR
python src/parse_llvm_ir.py benchmarks/simple_loop.ll

# Open the validation notebook
jupyter notebook notebooks/01_pipeline_validation.ipynb
```

## Project Structure

```
ml-loop-unrolling/
├── benchmarks/              # C programs for benchmarking
│   └── simple_loop.c        # Example program
├── data/
│   ├── raw/                # Raw benchmark results and features
│   └── processed/          # Cleaned datasets for ML
├── notebooks/              # Jupyter notebooks
│   └── 01_pipeline_validation.ipynb  # End-to-end validation
├── src/                    # Python source code
│   ├── __init__.py
│   ├── compile_and_measure.py  # Compilation and benchmarking
│   └── parse_llvm_ir.py        # LLVM IR feature extraction
├── pyproject.toml          # Python package configuration
├── requirements.txt        # Python dependencies
├── SETUP.md               # Detailed setup instructions
└── README.md              # This file
```

## Pipeline Overview

### 1. Compile to LLVM IR
```bash
clang -O0 -S -emit-llvm program.c -o program.ll
```

### 2. Extract Loop Features
- Instruction counts (loads, stores, arithmetic, branches)
- Trip count estimation
- Memory dependencies
- Control flow characteristics

### 3. Measure Performance
- Compile with unrolling: `clang -O3 -funroll-loops`
- Compile without: `clang -O3 -fno-unroll-loops`
- Time both versions (multiple runs with warmup)

### 4. Create Labels
- `speedup = time_no_unroll / time_unroll`
- `beneficial = speedup > 1.05` (5% threshold)

### 5. Train ML Model
- Features: loop characteristics from LLVM IR
- Labels: whether unrolling was beneficial
- Models: Logistic Regression, Decision Trees, Random Forest

## Next Steps

- [ ] Collect more diverse benchmark programs
- [ ] Expand feature extraction (data dependencies, vectorization potential)
- [ ] Build training dataset with 100+ loops
- [ ] Train baseline ML models
- [ ] Extract LLVM's unrolling decisions for comparison
- [ ] Evaluate model accuracy vs LLVM heuristics

## Contributing

This is a research/learning project. Contributions and suggestions welcome!

## License

MIT License - feel free to use and modify.
