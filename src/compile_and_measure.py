#!/usr/bin/env python3
"""
Compile C programs with different optimization flags and measure performance.
"""

import os
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Dict, Optional, Tuple


class CompilationError(Exception):
    """Raised when compilation fails."""
    pass


class BenchmarkRunner:
    """Compiles and benchmarks C programs with different unrolling strategies."""

    def __init__(self, clang_path: str = "clang", opt_level: str = "O3"):
        """
        Initialize the benchmark runner.

        Args:
            clang_path: Path to clang compiler (default: "clang")
            opt_level: Optimization level (default: "O3")
        """
        self.clang = clang_path
        self.opt_level = opt_level
        self._verify_clang()

    def _verify_clang(self):
        """Verify that clang is available."""
        try:
            result = subprocess.run(
                [self.clang, "--version"],
                capture_output=True,
                text=True,
                check=True,
            )
            print(f"Using: {result.stdout.splitlines()[0]}")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise RuntimeError(f"clang not found at '{self.clang}': {e}")

    def compile_to_llvm_ir(
        self,
        source_file: Path,
        output_file: Optional[Path] = None,
        opt_level: str = "0",
    ) -> Path:
        """
        Compile C source to LLVM IR (.ll file).

        Args:
            source_file: Path to C source file
            output_file: Output path for .ll file (auto-generated if None)
            opt_level: Optimization level (default: "0" for unoptimized IR)

        Returns:
            Path to the generated .ll file
        """
        if output_file is None:
            output_file = source_file.with_suffix(".ll")

        cmd = [
            self.clang,
            f"-{opt_level}",
            "-S",
            "-emit-llvm",
            str(source_file),
            "-o",
            str(output_file),
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise CompilationError(
                f"Failed to compile {source_file} to LLVM IR:\n{e.stderr}"
            )

        return output_file

    def compile_with_unrolling(
        self,
        source_file: Path,
        enable_unroll: bool,
        output_binary: Optional[Path] = None,
    ) -> Path:
        """
        Compile C source with or without loop unrolling.

        Args:
            source_file: Path to C source file
            enable_unroll: If True, enable loop unrolling; if False, disable it
            output_binary: Output path for binary (auto-generated if None)

        Returns:
            Path to the compiled binary
        """
        if output_binary is None:
            suffix = "_unroll" if enable_unroll else "_no_unroll"
            output_binary = source_file.with_suffix(suffix)

        unroll_flag = "-funroll-loops" if enable_unroll else "-fno-unroll-loops"

        cmd = [
            self.clang,
            f"-{self.opt_level}",
            unroll_flag,
            str(source_file),
            "-o",
            str(output_binary),
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise CompilationError(
                f"Failed to compile {source_file} with unroll={enable_unroll}:\n{e.stderr}"
            )

        return output_binary

    def measure_execution_time(
        self,
        binary: Path,
        num_runs: int = 10,
        warmup_runs: int = 2,
    ) -> Dict[str, float]:
        """
        Measure execution time of a binary.

        Args:
            binary: Path to compiled binary
            num_runs: Number of measurement runs
            warmup_runs: Number of warmup runs (not included in average)

        Returns:
            Dict with 'mean', 'min', 'max', 'std' execution times in seconds
        """
        if not binary.exists():
            raise FileNotFoundError(f"Binary not found: {binary}")

        times = []

        # Warmup runs
        for _ in range(warmup_runs):
            subprocess.run([str(binary)], capture_output=True, check=True)

        # Measurement runs
        for _ in range(num_runs):
            start = time.perf_counter()
            subprocess.run([str(binary)], capture_output=True, check=True)
            end = time.perf_counter()
            times.append(end - start)

        import numpy as np

        return {
            "mean": np.mean(times),
            "min": np.min(times),
            "max": np.max(times),
            "std": np.std(times),
            "runs": num_runs,
        }

    def benchmark_unrolling_impact(
        self,
        source_file: Path,
        num_runs: int = 10,
        warmup_runs: int = 2,
    ) -> Dict:
        """
        Benchmark the impact of loop unrolling on a C program.

        Args:
            source_file: Path to C source file
            num_runs: Number of measurement runs per configuration
            warmup_runs: Number of warmup runs per configuration

        Returns:
            Dict with compilation info, timing results, and speedup
        """
        print(f"\n{'='*60}")
        print(f"Benchmarking: {source_file.name}")
        print(f"{'='*60}")

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Compile both versions
            print("\n[1/4] Compiling with loop unrolling enabled...")
            binary_unroll = self.compile_with_unrolling(
                source_file,
                enable_unroll=True,
                output_binary=tmpdir / "prog_unroll",
            )

            print("[2/4] Compiling with loop unrolling disabled...")
            binary_no_unroll = self.compile_with_unrolling(
                source_file,
                enable_unroll=False,
                output_binary=tmpdir / "prog_no_unroll",
            )

            # Measure performance
            print(f"[3/4] Measuring with unrolling ({num_runs} runs + {warmup_runs} warmup)...")
            time_unroll = self.measure_execution_time(binary_unroll, num_runs, warmup_runs)

            print(f"[4/4] Measuring without unrolling ({num_runs} runs + {warmup_runs} warmup)...")
            time_no_unroll = self.measure_execution_time(
                binary_no_unroll, num_runs, warmup_runs
            )

            # Calculate speedup
            speedup = time_no_unroll["mean"] / time_unroll["mean"]

            results = {
                "source_file": str(source_file),
                "opt_level": self.opt_level,
                "with_unroll": time_unroll,
                "without_unroll": time_no_unroll,
                "speedup": speedup,
                "beneficial": speedup > 1.05,  # 5% threshold
            }

            # Print summary
            print(f"\n{'Results':^60}")
            print("-" * 60)
            print(f"  With unrolling:    {time_unroll['mean']*1000:8.3f} ms "
                  f"(± {time_unroll['std']*1000:.3f} ms)")
            print(f"  Without unrolling: {time_no_unroll['mean']*1000:8.3f} ms "
                  f"(± {time_no_unroll['std']*1000:.3f} ms)")
            print(f"  Speedup:           {speedup:8.3f}x")
            print(f"  Beneficial:        {'YES' if results['beneficial'] else 'NO'}")
            print("=" * 60)

            return results


def main():
    """Example usage."""
    import argparse

    parser = argparse.ArgumentParser(description="Benchmark loop unrolling impact")
    parser.add_argument("source_file", type=Path, help="C source file to benchmark")
    parser.add_argument(
        "--runs", type=int, default=10, help="Number of measurement runs (default: 10)"
    )
    parser.add_argument(
        "--warmup", type=int, default=2, help="Number of warmup runs (default: 2)"
    )
    parser.add_argument(
        "--opt", default="O3", help="Optimization level (default: O3)"
    )
    parser.add_argument(
        "--clang", default="clang", help="Path to clang compiler"
    )

    args = parser.parse_args()

    runner = BenchmarkRunner(clang_path=args.clang, opt_level=args.opt)

    # Generate LLVM IR
    print(f"\nGenerating LLVM IR for {args.source_file}...")
    ir_file = runner.compile_to_llvm_ir(args.source_file)
    print(f"  → {ir_file}")

    # Benchmark
    results = runner.benchmark_unrolling_impact(
        args.source_file,
        num_runs=args.runs,
        warmup_runs=args.warmup,
    )

    return results


if __name__ == "__main__":
    main()
