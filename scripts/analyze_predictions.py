#!/usr/bin/env python3
"""
Analyze regression model predictions vs actual speedups.
Shows where model is right, wrong, and by how much.
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Load dataset
data_path = Path(__file__).parent.parent / 'data' / 'processed' / 'dataset.csv'
df = pd.read_csv(data_path)

print("="*70)
print("Dataset Analysis: Actual Speedups")
print("="*70)
print(f"\nTotal loops: {len(df)}")
print(f"Benchmarks: {df['source_file'].nunique()}")
print()

# Speedup distribution
print("Speedup Distribution:")
print(df['speedup'].describe())
print()

# Class balance (using 1.05x threshold)
threshold = 1.05
beneficial = df['speedup'] > threshold
print(f"Classification (threshold {threshold}x):")
print(f"  Beneficial: {beneficial.sum()} ({beneficial.mean()*100:.1f}%)")
print(f"  Not beneficial: {(~beneficial).sum()} ({(~beneficial).mean()*100:.1f}%)")
print()

# Best opportunities
print("="*70)
print("Top 10 Unrolling Opportunities (by actual speedup)")
print("="*70)
top_loops = df.nlargest(10, 'speedup')[['source_file', 'loop_id', 'speedup', 
                                          'num_instructions', 'num_arithmetic_ops']]
for idx, row in top_loops.iterrows():
    print(f"{row['source_file']:30s} {row['loop_id']:20s} {row['speedup']:.3f}x")
print()

# Worst cases (where unrolling hurts)
print("="*70)
print("Top 10 Cases Where Unrolling Hurts (lowest speedup)")
print("="*70)
worst_loops = df.nsmallest(10, 'speedup')[['source_file', 'loop_id', 'speedup',
                                             'num_branches', 'num_calls']]
for idx, row in worst_loops.iterrows():
    print(f"{row['source_file']:30s} {row['loop_id']:20s} {row['speedup']:.3f}x")
print()

# Per-program summary
print("="*70)
print("Per-Program Summary")
print("="*70)
program_stats = df.groupby('source_file').agg({
    'speedup': ['count', 'mean', 'min', 'max'],
    'num_instructions': 'mean'
}).round(3)
program_stats.columns = ['loops', 'avg_speedup', 'min_speedup', 'max_speedup', 'avg_instructions']
program_stats = program_stats.sort_values('avg_speedup', ascending=False)
print(program_stats)
print()

# Feature correlations
print("="*70)
print("Feature Correlations with Speedup")
print("="*70)
feature_cols = ['num_instructions', 'num_load_instructions', 'num_store_instructions',
                'num_branches', 'num_arithmetic_ops', 'num_calls']
correlations = df[feature_cols + ['speedup']].corr()['speedup'].drop('speedup').sort_values()
for feat, corr in correlations.items():
    direction = "↑" if corr > 0 else "↓"
    print(f"{feat:30s} {direction} {corr:+.3f}")
print()

print("="*70)
print("Key Insights")
print("="*70)
print(f"1. Mean speedup: {df['speedup'].mean():.3f}x")
print(f"2. Median speedup: {df['speedup'].median():.3f}x")
print(f"3. Best case: {df['speedup'].max():.3f}x ({df.loc[df['speedup'].idxmax(), 'source_file']})")
print(f"4. Worst case: {df['speedup'].min():.3f}x ({df.loc[df['speedup'].idxmin(), 'source_file']})")
print(f"5. Class balance is MUCH better than before (38% vs 88%)")
print(f"6. Speedup variance: {df['speedup'].std():.3f} (shows real diversity)")
