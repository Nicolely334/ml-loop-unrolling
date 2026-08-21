# Getting Started with ML Loop Unrolling

## What's Been Set Up

Your project is now ready with a complete pipeline for measuring and predicting loop unrolling performance! Here's what was created:

### 📁 Project Structure

```
ml-loop-unrolling/
├── src/
│   ├── compile_and_measure.py    ✅ Compiles & benchmarks C programs
│   ├── parse_llvm_ir.py          ✅ Extracts loop features from LLVM IR
│   └── __init__.py               ✅ Package initialization
│
├── notebooks/
│   └── 01_pipeline_validation.ipynb  ✅ End-to-end validation notebook
│
├── benchmarks/
│   └── simple_loop.c             ✅ Example benchmark program
│
├── data/
│   ├── raw/                      ✅ For raw benchmark results
│   └── processed/                ✅ For cleaned ML datasets
│
├── pyproject.toml                ✅ Python package config
├── requirements.txt              ✅ Python dependencies
├── SETUP.md                      ✅ Installation guide
├── README.md                     ✅ Project overview
├── verify_setup.py               ✅ Setup verification script
└── .gitignore                    ✅ Git ignore rules
```

## Installation Steps

### 1. Install LLVM/Clang

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y clang llvm
```

**macOS (Homebrew):**
```bash
brew install llvm
```

**Arch Linux:**
```bash
sudo pacman -S clang llvm
```

### 2. Install Python Dependencies

```bash
cd /home/nicole/Dev/ml-loop-unrolling
pip install -r requirements.txt
```

Or for editable install:
```bash
pip install -e .
```

### 3. Verify Installation

```bash
python verify_setup.py
```

You should see all checks pass (✓) when ready.

## Running Your First Experiment

### Option 1: Command Line

```bash
# Step 1: Compile and benchmark simple_loop.c
python src/compile_and_measure.py benchmarks/simple_loop.c

# Step 2: Extract features from the generated LLVM IR
python src/parse_llvm_ir.py benchmarks/simple_loop.ll
```

### Option 2: Jupyter Notebook (Recommended)

```bash
# Launch Jupyter
jupyter notebook

# Open: notebooks/01_pipeline_validation.ipynb
# Run all cells to see the complete pipeline in action
```

The notebook will:
1. Compile `simple_loop.c` to LLVM IR
2. Show you the IR structure
3. Extract loop features
4. Benchmark with/without unrolling
5. Visualize the performance difference
6. Save results to `data/raw/`

## Understanding the Pipeline

### 1. Compilation (`compile_and_measure.py`)

**BenchmarkRunner** class provides:
- `compile_to_llvm_ir()` - Generates .ll files from C source
- `compile_with_unrolling()` - Creates binaries with `-funroll-loops` or `-fno-unroll-loops`
- `measure_execution_time()` - Times program execution with warmup runs
- `benchmark_unrolling_impact()` - Complete end-to-end benchmark

### 2. Feature Extraction (`parse_llvm_ir.py`)

**LLVMIRParser** class extracts:
- Basic counts: instructions, loads, stores, branches, calls
- Loop characteristics: trip count, nesting depth
- Data dependencies: phi nodes, memory accesses
- Control flow: exits, early exits

**Output:** `LoopFeatures` dataclass with 14 features per loop

### 3. Labels

Performance measurements create binary labels:
- `speedup = time_no_unroll / time_unroll`
- `beneficial = True` if `speedup > 1.05` (5% threshold)

## Next Steps

### Phase 1: Validate Pipeline ✅ (Done!)
- [x] Set up project structure
- [x] Create compilation tools
- [x] Create feature extraction
- [x] Create validation notebook

### Phase 2: Collect Data (Next!)
1. **Add more benchmark programs**
   - Create variations of loops (different sizes, patterns)
   - Use existing benchmark suites (PolyBench, MiBench)
   - Write custom loops with known characteristics

2. **Build dataset**
   ```bash
   # Example workflow for each program:
   python src/compile_and_measure.py benchmarks/program.c
   python src/parse_llvm_ir.py benchmarks/program.ll --output data/raw/program_features.csv
   ```

3. **Combine into training set**
   ```python
   import pandas as pd
   
   # Load all features
   features = []
   labels = []
   
   # Combine them
   df = pd.DataFrame(features)
   df['label'] = labels
   df.to_csv('data/processed/training_data.csv', index=False)
   ```

### Phase 3: Train ML Model
1. Create `notebooks/02_train_model.ipynb`
2. Train baseline models (Logistic Regression, Decision Tree)
3. Evaluate accuracy, precision, recall
4. Compare against LLVM's heuristics

### Phase 4: Improve
- Extract more sophisticated features
- Try ensemble models (Random Forest, XGBoost)
- Analyze which features matter most
- Test on real-world programs

## Quick Reference

### Run verification
```bash
python verify_setup.py
```

### Compile & benchmark a C file
```bash
python src/compile_and_measure.py path/to/program.c --runs 20
```

### Extract features from LLVM IR
```bash
python src/parse_llvm_ir.py path/to/program.ll --output features.csv
```

### Start Jupyter
```bash
jupyter notebook
```

## Troubleshooting

**"clang not found"**
- Install LLVM/Clang (see Installation Steps above)
- Check: `which clang`

**"ModuleNotFoundError: No module named 'numpy'"**
- Install dependencies: `pip install -r requirements.txt`

**"No loops detected"**
- The IR might be too optimized
- Try: `clang -O0` instead of `-O3` when generating IR

**Notebook kernel issues**
- Install kernel: `python -m ipykernel install --user --name ml-loop`
- Restart Jupyter

## Resources

- **LLVM IR Language Reference**: https://llvm.org/docs/LangRef.html
- **Loop Optimization in LLVM**: https://llvm.org/docs/Passes.html#loop-passes
- **scikit-learn Documentation**: https://scikit-learn.org/stable/

## Questions?

Check the detailed docs:
- `README.md` - Project overview
- `SETUP.md` - Installation guide
- `notebooks/01_pipeline_validation.ipynb` - Example usage

Happy experimenting! 🚀
