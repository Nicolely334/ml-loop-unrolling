# ML-Based Loop Unrolling Prediction

Using ml to help compilers decide when to unroll loops.

## Goal

This project aims to predict whether loop unrolling will improve program performance based on characteristics of the loop.

## Approach

1. Collect programs from the LLVM Test Suite
2. Identify loops in LLVM IR
3. Extract features from each loop
4. Measure performance with and without loop unrolling
5. Use the performance difference to create labels
6. Train a machine learning model to predict whether unrolling will help
7. Compare the ML model against LLVM's existing optimization behavior
## Tech Stack
- Python
- LLVM
- C/C++
- scikit-learn
- Jupyter
