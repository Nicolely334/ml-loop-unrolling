# ML Loop Unrolling Project - Status & Workflow

## ✅ Completed Setup

### 1. Project Structure
- ✅ Complete directory structure
- ✅ 11 diverse benchmark programs
- ✅ Python package configuration (`pyproject.toml`)
- ✅ Dependencies defined (`requirements.txt`)
- ✅ Git configuration (`.gitignore`)

### 2. Core Tools & Scripts
- ✅ **`src/compile_and_measure.py`** - Compilation and performance benchmarking
- ✅ **`src/parse_llvm_ir.py`** - Loop feature extraction from LLVM IR
- ✅ **`src/collect_dataset.py`** - Automated dataset collection
- ✅ **`src/predict.py`** - Prediction script for new programs
- ✅ **`verify_setup.py`** - Setup verification tool

### 3. Notebooks
- ✅ **`notebooks/01_pipeline_validation.ipynb`** - End-to-end pipeline validation
- ✅ **`notebooks/02_train_models.ipynb`** - Model training and evaluation

### 4. Documentation
- ✅ README.md - Project overview
- ✅ SETUP.md - Installation instructions
- ✅ GETTING_STARTED.md - Step-by-step guide
- ✅ benchmarks/README.md - Benchmark descriptions

## 🔄 Complete Workflow

### Phase 1: Setup ✅
```bash
# 1. Install LLVM/Clang
sudo apt install -y clang llvm

# 2. Install Python dependencies
cd /home/nicole/Dev/ml-loop-unrolling
pip install -r requirements.txt

# 3. Verify setup
python verify_setup.py
```

### Phase 2: Data Collection ⏳
```bash
# Collect dataset from all benchmarks
python src/collect_dataset.py --runs 20 --warmup 5

# Output: data/processed/dataset.csv
```

**What this does:**
- Compiles each benchmark to LLVM IR
- Extracts 14 loop features per loop
- Measures performance with/without unrolling
- Creates labeled dataset (beneficial = 1 or 0)

### Phase 3: Model Training ⏳
```bash
# Open training notebook
jupyter notebook notebooks/02_train_models.ipynb

# Run all cells to:
# - Explore dataset
# - Train Logistic Regression, Decision Tree, Random Forest
# - Evaluate performance
# - Save best model to models/best_model.pkl
```

### Phase 4: Prediction ⏳
```bash
# Predict on new program
python src/predict.py path/to/your_program.c

# Output: Recommendation (use -funroll-loops or not)
```

## 📊 Available Benchmarks (11 programs)

| Benchmark | Trip Count | Type | Expected Benefit |
|-----------|-----------|------|------------------|
| `simple_loop.c` | 100M | Simple | Medium |
| `small_loop.c` | 100 | Small | **HIGH** |
| `medium_loop.c` | 10K | Moderate compute | **HIGH** |
| `large_loop.c` | 100M | Very large | Low |
| `memory_intensive.c` | 1M | Memory-bound | Low |
| `compute_intensive.c` | 100K | Compute-heavy | **HIGH** |
| `loop_with_branch.c` | 50K | With conditionals | Medium |
| `nested_loop.c` | 1K × 100 | Nested | **HIGH** |
| `array_initialization.c` | 100K | Sequential stores | **HIGH** |
| `reduction.c` | 20 | Very small | Medium |
| `stride_access.c` | 10K | Strided access | Low |

## 🎯 Next Steps (To Do)

### Immediate Actions
1. **Install LLVM/Clang** (if not already installed)
   ```bash
   sudo apt install -y clang llvm
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run data collection**
   ```bash
   python src/collect_dataset.py --runs 20
   ```
   - Expected time: ~5-10 minutes
   - Output: `data/processed/dataset.csv`

4. **Train models**
   ```bash
   jupyter notebook notebooks/02_train_models.ipynb
   ```
   - Run all cells
   - Review model performance
   - Best model saved automatically

5. **Test prediction**
   ```bash
   python src/predict.py benchmarks/small_loop.c
   ```

### Future Enhancements

#### Short-term
- [ ] Add more benchmark programs (aim for 30+)
- [ ] Collect data from real-world codebases (LLVM Test Suite, SPEC)
- [ ] Implement hyperparameter tuning (GridSearchCV)
- [ ] Try ensemble methods (XGBoost, Stacking)

#### Medium-term
- [ ] Extract LLVM's unrolling decisions for comparison
- [ ] Add more sophisticated features:
  - Data dependency analysis
  - Vectorization potential
  - Register pressure estimation
  - Cache behavior prediction
- [ ] Create web UI for predictions
- [ ] Build LLVM pass integration

#### Long-term
- [ ] Multi-class prediction (unroll factors: 2, 4, 8, 16)
- [ ] Performance regression prediction (not just binary)
- [ ] Cross-architecture models (x86, ARM, etc.)
- [ ] Online learning (update model with new data)

## 📈 Expected Results

Based on the benchmark characteristics, we expect:

### Model Performance
- **Accuracy**: 70-85% (baseline)
- **Precision**: 75-90% (for "beneficial" class)
- **Recall**: 65-80% (catch most beneficial cases)

### Feature Importance (predicted)
1. **Trip count** - Strong indicator
2. **Instruction count** - Loop size matters
3. **Memory dependencies** - Memory-bound vs compute-bound
4. **Arithmetic operations** - Compute intensity
5. **Branches** - Control flow complexity

### Comparison to LLVM
- LLVM uses heuristics (trip count < 1000, etc.)
- ML model should capture more nuanced patterns
- Goal: Match or exceed LLVM's decisions

## 🔧 Troubleshooting

### "No loops detected"
- Try `-O0` instead of `-O3` when compiling to IR
- Check that the loop isn't optimized away

### Low model accuracy
- Collect more diverse benchmarks
- Check class balance (use SMOTE if imbalanced)
- Try feature engineering (ratios, derived features)

### Performance measurement noise
- Increase `--runs` (use 50+ for stable results)
- Ensure no other processes running
- Pin CPU frequency if available

## 📂 Project Files Summary

```
ml-loop-unrolling/
├── src/
│   ├── compile_and_measure.py   [429 lines] - Compilation & benchmarking
│   ├── parse_llvm_ir.py         [280 lines] - Feature extraction
│   ├── collect_dataset.py       [200 lines] - Automated data collection
│   └── predict.py               [200 lines] - Prediction script
│
├── benchmarks/                  [11 programs] - Diverse loop patterns
│
├── notebooks/
│   ├── 01_pipeline_validation.ipynb - Initial validation
│   └── 02_train_models.ipynb        - Model training
│
├── data/
│   ├── raw/        - Individual benchmark results
│   └── processed/  - Combined dataset (after collection)
│
└── models/         - Trained models (after training)
```

## 🚀 Quick Start Command Sequence

```bash
# From project root (/home/nicole/Dev/ml-loop-unrolling)

# 1. Verify setup
python verify_setup.py

# 2. Collect dataset (takes ~5-10 min)
python src/collect_dataset.py --runs 20

# 3. Train models
jupyter notebook notebooks/02_train_models.ipynb
# (Run all cells in browser)

# 4. Make prediction
python src/predict.py benchmarks/small_loop.c

# Done! You now have a working ML-based loop unrolling predictor.
```

## 📝 Notes

- All scripts are documented with docstrings
- All tools have `--help` flags for usage
- Data collection is idempotent (safe to re-run)
- Models are saved with pickle (Python 3.9+ compatible)

## 🎓 Learning Resources

- **LLVM IR**: https://llvm.org/docs/LangRef.html
- **Loop Optimizations**: https://llvm.org/docs/Passes.html#loop-passes
- **scikit-learn**: https://scikit-learn.org/stable/
- **Compiler Optimizations**: "Engineering a Compiler" by Cooper & Torczon

---

**Current Status**: ✅ **Ready for data collection and training!**

Just install dependencies and run the workflow above.
