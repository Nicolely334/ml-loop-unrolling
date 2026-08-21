# PolyBench-Inspired Benchmarks

Simplified standalone versions of classic PolyBench kernels.

## Programs

| File | Type | Loops | Pattern |
|------|------|-------|---------|
| `matrix_multiply.c` | Linear algebra | Triply nested | Dense computation, good ILP |
| `jacobi_2d.c` | Stencil | Doubly nested | Memory-intensive, regular access |
| `heat_3d.c` | Stencil | Triply nested | 3D spatial, cache-sensitive |
| `correlation.c` | Data mining | Multiple nested | Mix of reduction and nested |
| `floyd_warshall.c` | Graph | Triply nested | Loop-carried dependencies |
| `cholesky.c` | Linear algebra | Triangular | Non-uniform bounds |
| `atax.c` | BLAS | Doubly nested | Matrix-vector ops |

## Characteristics

- **Matrix multiply**: Classic n³ algorithm, inner loop benefits from unrolling
- **Jacobi 2D**: 5-point stencil, memory-bound, unrolling may not help
- **Heat 3D**: 7-point stencil in 3D, very memory-intensive
- **Correlation**: Statistical computation, mix of patterns
- **Floyd-Warshall**: Data dependencies limit unrolling benefit
- **Cholesky**: Triangular loops with varying bounds
- **ATAX**: Two passes (A*x then A^T*tmp), moderate size

All sized for ~0.5-2 second runtime to keep data collection fast.

## Differences from Original PolyBench

- Standalone (no polybench.h dependency)
- Fixed small dataset sizes (MINI/SMALL equivalent)
- Simplified - just the kernel + simple init
- Self-contained malloc/free (no polybench macros)

Based on PolyBench/C 4.2.1: http://polybench.sourceforge.net
