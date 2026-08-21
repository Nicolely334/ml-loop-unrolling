# Results

## What Changed

Started with binary classification (beneficial/not) but that was pointless - 88.7% of loops were beneficial, so you could just always predict "yes" and get 88.7% accuracy. The ML model got 92.3% which sounds good but is only 3.6% better than the dumb baseline.

Switched to **regression** instead - predict the actual speedup number (like 1.15x or 0.92x). Much more useful.

Also added 10 more benchmarks to get better diversity.

## Dataset

- **84 loops** from 28 C programs
- Speedup range: **0.840x to 1.375x** (unrolling can actually hurt!)
- Mean: 1.078x, Median: 1.035x
- Using 1.05x threshold: 38% beneficial, 62% not (way better balance than before)

## What Works, What Doesn't

**Best unrolling candidates:**
- jacobi_2d (1.375x) - 2D stencil pattern
- floyd_warshall (1.287x) - graph algorithm
- accumulator (1.186x)
- dot_product (1.131x)

Pattern: regular memory access, arithmetic-heavy, few branches

**Worst (unrolling hurts performance):**
- loop_with_branch (0.840x) - conditional in loop body
- bitcount (0.900x) - unpredictable inner loop
- nested_loop (0.945x)
- polynomial (0.952x)

Pattern: branches, irregular patterns, memory-bound

**Feature correlations are weak** - most features don't vary much. Need better engineered features (ratios, log transforms).

## Model

Random Forest regressor with engineered features (memory_ratio, compute_ratio, trip_count_log).

Run `notebooks/04_regression_model.ipynb` for training and metrics.

## Why Regression > Classification

Binary classification throws away information - a 1.06x speedup and 1.35x speedup are both just "beneficial". Can't rank or prioritize.

Regression predicts the actual number, so you can:
- Rank loops by predicted benefit
- Focus optimization on high-value targets
- Set dynamic thresholds
- MAE is easy to interpret ("avg wrong by 0.05x")

## Use Cases

```python
# 1. Rank loops, unroll top 10%
predictions = model.predict(features)
top_loops = np.argsort(predictions)[-10:]

# 2. Cost-benefit
if predicted_speedup > 1.1 and loop_size < 100:
    unroll(loop)

# 3. Replace LLVM heuristics for domain-specific code
```

## LLVM Comparison

Hard to compare directly - LLVM only logs loops it *actually unrolls* via `-Rpass=loop-unroll`, not the ones it skips.

Could measure with `-funroll-loops` vs `-fno-unroll-loops` and compare predictions to LLVM's choices. Find disagreements and see who's right.

TODO for future work.

## TODO

1. More data - SPEC CPU, LLVM test suite (target 500+ loops)
2. Better features - instruction mix percentages, stride patterns
3. Multi-class - predict unroll factor (2x, 4x, 8x) instead of just speedup
4. LLVM pass - integrate as actual compiler optimization

## Running

```bash
# collect data
python3 src/collect_dataset.py --runs 10

# analyze
python3 scripts/analyze_predictions.py

# train
jupyter notebook notebooks/04_regression_model.ipynb
```

## Summary

**Before**: 92.3% classification accuracy (but 88.7% baseline - basically useless)

**After**: Regression predicting actual speedup 0.84x-1.37x
- Balanced dataset (38% vs 62%)
- Can rank loops by benefit
- Clear patterns: stencils win, branches lose

Regression is way more useful than binary classification for this problem.
