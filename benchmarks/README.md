# Benchmarks

18 C programs with different loop patterns for testing unrolling prediction.

## Structure

- `*.c` - 11 basic benchmarks with simple patterns
- `polybench/*.c` - 7 PolyBench-inspired kernels (see `polybench/README.md`)

## Programs

| File | Trip Count | Type | Expected to benefit? |
|------|-----------|------|---------------------|
| `small_loop.c` | 100 | Tiny loop | Yes - overhead reduction |
| `medium_loop.c` | 10K | Moderate | Yes |
| `large_loop.c` | 100M | Huge | No - code bloat |
| `memory_intensive.c` | 1M | Memory-bound | No |
| `compute_intensive.c` | 100K | Arithmetic-heavy | Yes - ILP |
| `loop_with_branch.c` | 50K | Has conditional | Maybe |
| `nested_loop.c` | 1K × 100 | Nested | Yes (inner loop) |
| `array_initialization.c` | 100K | Sequential stores | Yes |
| `reduction.c` | 20 | Very small | Maybe |
| `stride_access.c` | 10K | Non-sequential | No |
| `simple_loop.c` | 100M | Basic | Maybe |

## Running

```bash
# Single benchmark
python src/compile_and_measure.py benchmarks/small_loop.c

# All benchmarks (finds recursively)
python src/collect_dataset.py --runs 20

# Expected: ~30-50 loops total (some programs have multiple loops)
```

## Notes

- All use printf() to prevent dead code elimination
- Trip counts chosen for ~0.1-1s runtime
- No external dependencies beyond libc
