#!/usr/bin/env python3

import pandas as pd
import numpy as np
from pathlib import Path

data_path = Path(__file__).parent.parent / 'data' / 'processed' / 'dataset.csv'
df = pd.read_csv(data_path)

print(f"\nDataset: {len(df)} loops from {df['source_file'].nunique()} programs")
print("="*70)

print("\nSpeedup stats:")
print(df['speedup'].describe())

threshold = 1.05
beneficial = df['speedup'] > threshold
print(f"\nUsing {threshold}x threshold:")
print(f"  Beneficial: {beneficial.sum()} ({beneficial.mean()*100:.1f}%)")
print(f"  Not: {(~beneficial).sum()} ({(~beneficial).mean()*100:.1f}%)")

print("\n" + "="*70)
print("Best unrolling candidates:")
print("="*70)
top = df.nlargest(5, 'speedup')[['source_file', 'speedup']]
for idx, row in top.iterrows():
    print(f"{row['source_file']:30s} {row['speedup']:.3f}x")

print("\nWorst cases (unrolling hurts):")
print("="*70)
worst = df.nsmallest(5, 'speedup')[['source_file', 'speedup']]
for idx, row in worst.iterrows():
    print(f"{row['source_file']:30s} {row['speedup']:.3f}x")

print("\n" + "="*70)
print("Per-program summary (sorted by avg speedup):")
print("="*70)
stats = df.groupby('source_file')['speedup'].agg(['count', 'mean']).round(3)
stats.columns = ['loops', 'avg_speedup']
stats = stats.sort_values('avg_speedup', ascending=False)
print(stats.head(15))

print("\n" + "="*70)
print("Summary:")
print(f"  Mean speedup: {df['speedup'].mean():.3f}x")
print(f"  Median: {df['speedup'].median():.3f}x")
print(f"  Best: {df['speedup'].max():.3f}x")
print(f"  Worst: {df['speedup'].min():.3f}x")
print(f"  Std dev: {df['speedup'].std():.3f}")
print("="*70)
