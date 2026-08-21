# Results & Analysis

## Project Evolution

### Phase 1: Binary Classification (Initial)
- **Dataset**: 62 loops from 18 benchmarks
- **Problem**: 88.7% beneficial (too easy, just predict "always unroll")
- **Metric**: 92.3% accuracy (only 3.6% better than baseline)
- **Conclusion**: Not useful - baseline is too high

### Phase 2: Regression + Expanded Dataset ✅
- **Dataset**: **84 loops from 28 benchmarks**
- **Balance**: **38.1% beneficial, 61.9% not** (much better!)
- **Metric**: **Predict actual speedup** (0.840x to 1.375x range)
- **Approach**: Random Forest Regressor, MAE as evaluation metric

## Dataset Summary

| Metric | Value |
|--------|-------|
| **Total loops** | 84 |
| **Benchmarks** | 28 programs |
| **Speedup range** | 0.840x - 1.375x |
| **Mean speedup** | 1.078x |
| **Median speedup** | 1.035x |
| **Std deviation** | 0.141 |
| **Beneficial (>1.05x)** | 32 loops (38.1%) |
| **Not beneficial** | 52 loops (61.9%) |

## Key Insights

### 1. What Makes Unrolling Beneficial?

**Best cases (>1.28x speedup):**
- `jacobi_2d.c` - 1.375x (2D stencil, regular memory access)
- `floyd_warshall.c` - 1.287x (graph shortest path)
- `accumulator.c` - 1.186x (simple accumulation)
- `dot_product.c` - 1.131x (vector multiply-add)

**Common patterns:**
- Regular memory access patterns
- High arithmetic intensity
- Few branches
- Predictable trip counts

### 2. When Unrolling Hurts

**Worst cases (<0.95x speedup):**
- `loop_with_branch.c` - 0.840x (conditional inside loop)
- `bitcount.c` - 0.900x (inner while loop, unpredictable)
- `nested_loop.c` - 0.945x (complex nesting)
- `polynomial.c` - 0.952x (short dependency chain)

**Common patterns:**
- Branches/conditionals inside loops
- Irregular access patterns
- Small trip counts
- Memory-bound operations (cache thrashing)

### 3. Feature Correlations

Weak correlations found (most features constant across loops):
- `num_load/store_instructions`: slight negative correlation
- Need better engineered features (ratios, log transforms)

## Regression Model Performance

Using engineered features (memory_ratio, compute_ratio, trip_count_log, etc.):

| Model | MAE | R² | Notes |
|-------|-----|-----|-------|
| **Random Forest** | TBD | TBD | Best for non-linear patterns |
| **Ridge** | TBD | TBD | Regularized linear |
| **Decision Tree** | TBD | TBD | Interpretable |

*(Run `notebooks/04_regression_model.ipynb` to see actual metrics)*

## Why This Approach is Better

### Binary Classification Problems:
1. ❌ Throws away information (1.06x and 1.35x both "beneficial")
2. ❌ Threshold arbitrary (why 1.05x?)
3. ❌ Can't prioritize high-value loops
4. ❌ Imbalanced dataset makes metrics misleading

### Regression Advantages:
1. ✅ Predicts actual speedup magnitude
2. ✅ Can rank loops by predicted benefit
3. ✅ More useful for compiler decisions ("focus on top 10%")
4. ✅ MAE is interpretable ("avg error is 0.05x")
5. ✅ Can set threshold dynamically based on context

## Practical Use Cases

### 1. Loop Ranking
```python
# Predict all loops, sort by speedup, unroll top N%
predictions = model.predict(loop_features)
top_loops = np.argsort(predictions)[-10:]  # top 10%
```

### 2. Cost-Benefit Analysis
```python
# Only unroll if predicted benefit > code size cost
if predicted_speedup > 1.1 and loop_size < 100:
    unroll(loop)
```

### 3. Compiler Integration
```python
# Replace LLVM's hard-coded heuristics with ML
# Especially useful for domain-specific workloads
```

## Comparison: ML vs LLVM

**Challenge**: LLVM only reports loops it *actually unrolls* (via `-Rpass=loop-unroll`).
It doesn't log decisions to *not* unroll, making direct comparison difficult.

**Alternative approach**: 
- Measure speedup with LLVM's `-funroll-loops` vs `-fno-unroll-loops`
- Compare our predictions to LLVM's choices
- Find cases where we disagree and measure which is better

## Next Steps to Improve

1. **More data** (target: 500+ loops)
   - SPEC CPU benchmarks
   - LLVM test suite
   - Real codebases

2. **Better features**
   - Instruction mix (% loads, % stores, % arithmetic)
   - Memory access stride patterns
   - Loop nesting depth
   - Function call overhead

3. **Multi-class prediction**
   - Predict unroll factor (2x, 4x, 8x, 16x)
   - More realistic than binary

4. **LLVM integration**
   - Build as LLVM analysis pass
   - Compare against built-in heuristics
   - A/B test on real workloads

## Files

| File | Purpose |
|------|---------|
| `notebooks/04_regression_model.ipynb` | Regression model training & analysis |
| `notebooks/03_data_analysis.ipynb` | Feature engineering & exploration |
| `scripts/analyze_predictions.py` | Dataset summary & insights |
| `scripts/add_more_benchmarks.sh` | Generate 10 additional benchmarks |
| `data/processed/dataset.csv` | 84 loops × 22 features + speedup |

## How to Reproduce

```bash
# 1. Collect data (requires clang/LLVM)
python3 src/collect_dataset.py --runs 10

# 2. Analyze dataset
python3 scripts/analyze_predictions.py

# 3. Train regression model
jupyter notebook notebooks/04_regression_model.ipynb

# 4. Compare features
python3 src/quick_train.py  # quick baseline
```

## Conclusion

**Is this project viable?**

**Before**: No - 92.3% accuracy on 88.7% baseline is meaningless.

**After**: Yes - predicting actual speedup (0.84x-1.37x) with:
- Balanced dataset (38/62 split)
- Interpretable metric (MAE = avg error in speedup)
- Practical use (rank loops, dynamic thresholds)
- Clear patterns (stencils good, branches bad)

**Best results**: jacobi_2d (1.375x), floyd_warshall (1.287x)  
**Worst results**: loop_with_branch (0.840x), bitcount (0.900x)

The regression approach captures **real compiler insights** that binary classification missed.
