# Benchmark Programs

This directory contains C programs with diverse loop characteristics for training the ML model.

## Benchmark Descriptions

| Benchmark | Trip Count | Characteristics | Expected Unrolling Benefit |
|-----------|-----------|-----------------|---------------------------|
| `simple_loop.c` | 100M | Very simple accumulation | Medium - large trip count |
| `small_loop.c` | 100 | Small, compute-light | **HIGH** - overhead reduction |
| `medium_loop.c` | 10K | Moderate computation | **HIGH** - good balance |
| `large_loop.c` | 100M | Very large, simple | Low - unrolling overhead |
| `memory_intensive.c` | 1M | Heavy memory loads/stores | Low - memory bottleneck |
| `compute_intensive.c` | 100K | Floating-point arithmetic | **HIGH** - ILP benefits |
| `loop_with_branch.c` | 50K | Conditional inside loop | Medium - branch prediction |
| `nested_loop.c` | 1K × 100 | Two-level nesting | **HIGH** - inner loop candidate |
| `array_initialization.c` | 100K | Sequential store pattern | **HIGH** - vectorizable |
| `reduction.c` | 20 | Very small, data dependency | Medium - small overhead |
| `stride_access.c` | 10K | Strided memory access | Low - cache misses |

## Loop Pattern Coverage

### By Trip Count
- **Small (< 1K)**: `small_loop`, `reduction`
- **Medium (1K-100K)**: `medium_loop`, `compute_intensive`, `loop_with_branch`, `array_initialization`, `stride_access`
- **Large (> 100K)**: `simple_loop`, `large_loop`, `memory_intensive`

### By Computation Type
- **Arithmetic-heavy**: `compute_intensive`, `medium_loop`
- **Memory-heavy**: `memory_intensive`, `stride_access`
- **Mixed**: `array_initialization`, `simple_loop`
- **Minimal**: `small_loop`, `large_loop`

### By Control Flow
- **Simple**: Most benchmarks
- **With branches**: `loop_with_branch`
- **Nested**: `nested_loop`

### By Memory Pattern
- **No memory**: `small_loop`, `reduction`
- **Sequential access**: `memory_intensive`, `array_initialization`
- **Strided access**: `stride_access`

## Expected Results

Based on compiler optimization theory:

**Should benefit from unrolling:**
- Small loops with low overhead (< 1000 iterations)
- Compute-intensive loops (more ILP)
- Sequential memory access (vectorization)
- Inner loops of nested structures

**Should NOT benefit from unrolling:**
- Very large loops (code bloat, I-cache pollution)
- Memory-bound loops (bottleneck elsewhere)
- Loops with complex control flow
- Strided/random memory access

## Adding New Benchmarks

When creating new benchmarks:
1. Focus on realistic code patterns
2. Ensure the loop actually executes (optimizer might eliminate dead code)
3. Use `printf()` to prevent aggressive optimization
4. Document the expected unrolling behavior
5. Run through the pipeline to verify it compiles and measures correctly

## Running Benchmarks

### Single benchmark
```bash
python src/compile_and_measure.py benchmarks/small_loop.c
```

### All benchmarks
```bash
python src/collect_dataset.py --benchmarks-dir benchmarks --runs 20
```

## Notes

- All programs are self-contained (no external dependencies except stdlib/math)
- Programs are intentionally simple to isolate loop characteristics
- Trip counts are tuned to complete in reasonable time (< 1 second per run)
- Memory allocation benchmarks use `malloc/free` to prevent stack overflow
