#!/usr/bin/env python3
"""
Automated data collection script for the loop unrolling prediction dataset.

This script:
1. Finds all C files in the benchmarks directory
2. For each file:
   - Compiles to LLVM IR
   - Extracts loop features
   - Measures performance with/without unrolling
   - Combines features with labels
3. Saves the complete dataset to CSV
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List

import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from compile_and_measure import BenchmarkRunner, CompilationError
from parse_llvm_ir import extract_features_from_ir


def collect_benchmark_data(
    source_file: Path,
    runner: BenchmarkRunner,
    num_runs: int = 10,
    warmup_runs: int = 2,
) -> List[Dict]:
    """
    Collect complete data for one benchmark program.

    Args:
        source_file: Path to C source file
        runner: BenchmarkRunner instance
        num_runs: Number of measurement runs
        warmup_runs: Number of warmup runs

    Returns:
        List of dictionaries with features + performance labels
    """
    print(f"\n{'=' * 70}")
    print(f"Processing: {source_file.name}")
    print(f"{'=' * 70}")

    try:
        # Step 1: Compile to LLVM IR
        print("[1/3] Compiling to LLVM IR...")
        ir_file = runner.compile_to_llvm_ir(source_file, opt_level="O0")

        # Step 2: Extract loop features
        print("[2/3] Extracting loop features...")
        loop_features = extract_features_from_ir(ir_file)

        if not loop_features:
            print(f"  ⚠️  No loops detected in {source_file.name}")
            return []

        print(f"  ✓ Found {len(loop_features)} loop(s)")

        # Step 3: Measure performance
        print(f"[3/3] Benchmarking ({num_runs} runs + {warmup_runs} warmup)...")
        perf_results = runner.benchmark_unrolling_impact(
            source_file,
            num_runs=num_runs,
            warmup_runs=warmup_runs,
        )

        # Combine features with performance labels
        dataset_entries = []
        for idx, features in enumerate(loop_features):
            entry = {
                "source_file": source_file.name,
                "loop_index": idx,
                **features,  # All loop features
                "time_with_unroll_ms": perf_results["with_unroll"]["mean"] * 1000,
                "time_without_unroll_ms": perf_results["without_unroll"]["mean"] * 1000,
                "speedup": perf_results["speedup"],
                "beneficial": int(perf_results["beneficial"]),
            }
            dataset_entries.append(entry)

        print(f"  ✓ Collected {len(dataset_entries)} dataset entry(ies)")
        return dataset_entries

    except CompilationError as e:
        print(f"  ✗ Compilation failed: {e}")
        return []
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return []


def main():
    parser = argparse.ArgumentParser(
        description="Collect loop unrolling dataset from benchmark programs"
    )
    parser.add_argument(
        "--benchmarks-dir",
        type=Path,
        default=Path(__file__).parent.parent / "benchmarks",
        help="Directory containing C benchmark files (searches recursively)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parent.parent / "data" / "processed" / "dataset.csv",
        help="Output CSV file",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=10,
        help="Number of measurement runs per benchmark (default: 10)",
    )
    parser.add_argument(
        "--warmup",
        type=int,
        default=2,
        help="Number of warmup runs (default: 2)",
    )
    parser.add_argument(
        "--opt",
        default="O3",
        help="Optimization level for performance benchmarking (default: O3)",
    )
    parser.add_argument(
        "--pattern",
        default="*.c",
        help="Glob pattern for C files (default: *.c)",
    )

    args = parser.parse_args()

    # Find all benchmark files (recursive search)
    benchmark_files = sorted(args.benchmarks_dir.rglob(args.pattern))

    if not benchmark_files:
        print(f"No benchmark files found in {args.benchmarks_dir} matching {args.pattern}")
        return 1

    print(f"\n{'=' * 70}")
    print(f"Loop Unrolling Dataset Collection")
    print(f"{'=' * 70}")
    print(f"Benchmarks directory: {args.benchmarks_dir}")
    print(f"Found {len(benchmark_files)} C file(s)")
    print(f"Measurement runs: {args.runs} (+ {args.warmup} warmup)")
    print(f"Optimization level: {args.opt}")
    print(f"Output file: {args.output}")
    print(f"{'=' * 70}")

    # Initialize benchmark runner
    runner = BenchmarkRunner(opt_level=args.opt)

    # Collect data from all benchmarks
    all_data = []
    successful = 0
    failed = 0

    for source_file in benchmark_files:
        entries = collect_benchmark_data(
            source_file,
            runner,
            num_runs=args.runs,
            warmup_runs=args.warmup,
        )

        if entries:
            all_data.extend(entries)
            successful += 1
        else:
            failed += 1

    # Create DataFrame
    if not all_data:
        print("\n❌ No data collected. Check compilation errors above.")
        return 1

    df = pd.DataFrame(all_data)

    # Ensure output directory exists
    args.output.parent.mkdir(parents=True, exist_ok=True)

    # Save to CSV
    df.to_csv(args.output, index=False)

    # Also save as JSON for reference
    json_output = args.output.with_suffix(".json")
    df.to_json(json_output, orient="records", indent=2)

    # Print summary
    print(f"\n{'=' * 70}")
    print(f"Collection Summary")
    print(f"{'=' * 70}")
    print(f"Total benchmarks processed: {len(benchmark_files)}")
    print(f"  ✓ Successful: {successful}")
    print(f"  ✗ Failed: {failed}")
    print(f"\nDataset statistics:")
    print(f"  Total loops: {len(df)}")
    print(f"  Beneficial (speedup > 1.05): {df['beneficial'].sum()} ({df['beneficial'].mean()*100:.1f}%)")
    print(f"  Not beneficial: {(1 - df['beneficial']).sum()} ({(1-df['beneficial'].mean())*100:.1f}%)")
    print(f"\nSpeedup statistics:")
    print(f"  Mean: {df['speedup'].mean():.3f}x")
    print(f"  Median: {df['speedup'].median():.3f}x")
    print(f"  Min: {df['speedup'].min():.3f}x")
    print(f"  Max: {df['speedup'].max():.3f}x")
    print(f"\nOutput files:")
    print(f"  CSV: {args.output}")
    print(f"  JSON: {json_output}")
    print(f"{'=' * 70}")

    # Show a preview
    print("\nDataset preview (first 5 rows):")
    print(df.head().to_string())

    return 0


if __name__ == "__main__":
    sys.exit(main())
