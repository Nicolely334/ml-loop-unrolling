#!/usr/bin/env python3

import subprocess
import tempfile
import time
from pathlib import Path
from typing import Dict, Optional


class CompilationError(Exception):
    pass


class BenchmarkRunner:
    def __init__(self, clang_path="clang", opt_level="O3"):
        self.clang = clang_path
        self.opt_level = opt_level
        self._verify_clang()

    def _verify_clang(self):
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

    def compile_to_llvm_ir(self, source_file: Path, output_file=None, opt_level="O0"):
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
            raise CompilationError(f"Failed to compile {source_file} to IR:\n{e.stderr}")

        return output_file

    def compile_with_unrolling(self, source_file: Path, enable_unroll: bool, output_binary=None):
        if output_binary is None:
            suffix = "_unroll" if enable_unroll else "_no_unroll"
            output_binary = source_file.with_suffix(suffix)

        unroll_flag = "-funroll-loops" if enable_unroll else "-fno-unroll-loops"
        cmd = [self.clang, f"-{self.opt_level}", unroll_flag, str(source_file), "-o", str(output_binary)]

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise CompilationError(f"Compilation failed:\n{e.stderr}")

        return output_binary

    def measure_execution_time(self, binary: Path, num_runs=10, warmup_runs=2):
        import numpy as np
        
        if not binary.exists():
            raise FileNotFoundError(f"Binary not found: {binary}")

        times = []
        
        # warmup
        for _ in range(warmup_runs):
            subprocess.run([str(binary)], capture_output=True, check=True)

        # actual measurements
        for _ in range(num_runs):
            start = time.perf_counter()
            subprocess.run([str(binary)], capture_output=True, check=True)
            times.append(time.perf_counter() - start)

        return {
            "mean": np.mean(times),
            "min": np.min(times),
            "max": np.max(times),
            "std": np.std(times),
            "runs": num_runs,
        }

    def benchmark_unrolling_impact(self, source_file: Path, num_runs=10, warmup_runs=2):
        print(f"\n{'='*60}")
        print(f"Benchmarking: {source_file.name}")
        print(f"{'='*60}")

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            print("\n[1/4] Compiling with unrolling...")
            binary_unroll = self.compile_with_unrolling(
                source_file, True, tmpdir / "prog_unroll"
            )

            print("[2/4] Compiling without unrolling...")
            binary_no_unroll = self.compile_with_unrolling(
                source_file, False, tmpdir / "prog_no_unroll"
            )

            print(f"[3/4] Measuring with unrolling ({num_runs} runs)...")
            time_unroll = self.measure_execution_time(binary_unroll, num_runs, warmup_runs)

            print(f"[4/4] Measuring without unrolling ({num_runs} runs)...")
            time_no_unroll = self.measure_execution_time(binary_no_unroll, num_runs, warmup_runs)

            speedup = time_no_unroll["mean"] / time_unroll["mean"]

            results = {
                "source_file": str(source_file),
                "opt_level": self.opt_level,
                "with_unroll": time_unroll,
                "without_unroll": time_no_unroll,
                "speedup": speedup,
                "beneficial": speedup > 1.05,  # TODO: make threshold configurable
            }

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
    import argparse

    parser = argparse.ArgumentParser(description="Benchmark loop unrolling")
    parser.add_argument("source_file", type=Path)
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--warmup", type=int, default=2)
    parser.add_argument("--opt", default="O3")
    parser.add_argument("--clang", default="clang")
    args = parser.parse_args()

    runner = BenchmarkRunner(clang_path=args.clang, opt_level=args.opt)

    print(f"\nGenerating IR...")
    ir_file = runner.compile_to_llvm_ir(args.source_file)
    print(f"  → {ir_file}")

    results = runner.benchmark_unrolling_impact(args.source_file, args.runs, args.warmup)
    return results


if __name__ == "__main__":
    main()
