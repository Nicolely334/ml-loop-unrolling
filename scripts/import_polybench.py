#!/usr/bin/env python3
# Extract standalone benchmarks from PolyBench

import re
import shutil
from pathlib import Path

POLYBENCH_ROOT = Path("/home/nicole/Dev/polybench")
OUTPUT_DIR = Path(__file__).parent.parent / "benchmarks" / "polybench"

# Select interesting benchmarks with diverse loop patterns
SELECTED_BENCHMARKS = [
    # Linear algebra - lots of nested loops
    "linear-algebra/blas/gemm/gemm.c",          # matrix multiply (triply nested)
    "linear-algebra/blas/gemver/gemver.c",      # vector operations
    "linear-algebra/solvers/cholesky/cholesky.c",  # triangular matrix
    "linear-algebra/kernels/2mm/2mm.c",         # 2 matrix multiplies
    "linear-algebra/kernels/atax/atax.c",       # matrix transpose
    
    # Stencils - regular access patterns
    "stencils/jacobi-2d/jacobi-2d.c",           # 2D iterative stencil
    "stencils/heat-3d/heat-3d.c",               # 3D heat equation
    "stencils/seidel-2d/seidel-2d.c",           # 2D Gauss-Seidel
    
    # Data mining - reduction patterns
    "datamining/correlation/correlation.c",      # statistical computation
    "datamining/covariance/covariance.c",       # covariance matrix
    
    # Medley - mixed patterns
    "medley/floyd-warshall/floyd-warshall.c",   # graph algorithm
    "medley/deriche/deriche.c",                 # image filter
]

# Small dataset sizes so benchmarks run fast
DATASET_SIZES = {
    "N": "40",
    "M": "40", 
    "P": "40",
    "TSTEPS": "20",
}


def extract_kernel_function(source_path):
    """Extract just the computational kernel from a PolyBench program"""
    
    content = source_path.read_text()
    
    # find the kernel function (usually named after the benchmark)
    # it's typically between init_array and print_array
    kernel_match = re.search(
        r'(/\*\* Main computational kernel.*?\*/.*?^}\s*$)',
        content,
        re.MULTILINE | re.DOTALL
    )
    
    if not kernel_match:
        # try to find any function that's not init/print/main
        return None
    
    return kernel_match.group(1)


def create_standalone_benchmark(source_path, output_path):
    """Create a simplified standalone version"""
    
    name = source_path.stem
    content = source_path.read_text()
    
    # extract the kernel
    kernel = extract_kernel_function(source_path)
    if not kernel:
        print(f"  ⚠️  Couldn't extract kernel from {name}, skipping")
        return False
    
    # create simplified standalone version
    standalone = f"""// Simplified from PolyBench: {source_path.relative_to(POLYBENCH_ROOT)}
// Original: http://polybench.sourceforge.net

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Dataset size (MINI for fast benchmarking)
#define N {DATASET_SIZES['N']}
#define M {DATASET_SIZES['M']}
#define TSTEPS {DATASET_SIZES['TSTEPS']}

typedef double DATA_TYPE;

{kernel}

int main() {{
    // TODO: add initialization and timing
    // For now just a placeholder
    printf("Benchmark: {name}\\n");
    return 0;
}}
"""
    
    output_path.write_text(standalone)
    return True


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Importing PolyBench programs...")
    print(f"Source: {POLYBENCH_ROOT}")
    print(f"Output: {OUTPUT_DIR}")
    print()
    
    success = 0
    failed = 0
    
    for bench_rel_path in SELECTED_BENCHMARKS:
        source = POLYBENCH_ROOT / bench_rel_path
        
        if not source.exists():
            print(f"❌ Not found: {bench_rel_path}")
            failed += 1
            continue
        
        output_name = source.stem + "_polybench.c"
        output = OUTPUT_DIR / output_name
        
        print(f"Processing {source.stem}...", end=" ")
        
        if create_standalone_benchmark(source, output):
            print(f"✓ → {output_name}")
            success += 1
        else:
            failed += 1
    
    print()
    print(f"Imported: {success} benchmarks")
    if failed:
        print(f"Failed: {failed}")
    
    # Actually, the extraction is tricky. Let me try a different approach:
    # just copy the files and modify compile_and_measure.py to handle polybench includes
    print()
    print("Note: Full extraction is complex. Consider simpler approach:")
    print("  1. Copy polybench utilities to benchmarks/polybench/")
    print("  2. Modify BenchmarkRunner to use -I flag for polybench programs")


if __name__ == "__main__":
    main()
