# Setup Guide

## Prerequisites

This project requires:
1. Python 3.9 or higher
2. LLVM/Clang toolchain (for compiling and analyzing programs)

## Installation

### 1. Install LLVM/Clang

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install -y clang llvm
```

#### macOS (Homebrew)
```bash
brew install llvm
```

#### Arch Linux
```bash
sudo pacman -S clang llvm
```

### 2. Verify LLVM Installation

```bash
clang --version
opt --version
```

You should see version information for both tools (LLVM 10+ recommended).

### 3. Install Python Dependencies

#### Option A: Using pip (recommended for development)
```bash
cd ml-loop-unrolling
pip install -e .
```

#### Option B: Using requirements.txt
```bash
cd ml-loop-unrolling
pip install -r requirements.txt
```

## Quick Start

### 1. Test the Pipeline

```bash
# Run the benchmark on simple_loop.c
python src/compile_and_measure.py benchmarks/simple_loop.c

# Extract LLVM IR features
python src/parse_llvm_ir.py benchmarks/simple_loop.ll
```

### 2. Run the Validation Notebook

```bash
jupyter notebook notebooks/01_pipeline_validation.ipynb
```

## Project Structure

```
ml-loop-unrolling/
├── benchmarks/          # C programs for benchmarking
├── data/
│   ├── raw/            # Raw benchmark results
│   └── processed/      # Cleaned datasets
├── notebooks/          # Jupyter notebooks for analysis
├── src/                # Python source code
│   ├── compile_and_measure.py   # Compilation and benchmarking
│   └── parse_llvm_ir.py         # LLVM IR feature extraction
├── pyproject.toml      # Python package configuration
└── README.md
```

## Troubleshooting

### "clang not found"
- Ensure LLVM/Clang is installed (see step 1)
- Add LLVM bin directory to your PATH if installed in a non-standard location

### "opt not found"
- The `opt` tool is part of LLVM
- On macOS with Homebrew: `export PATH="/usr/local/opt/llvm/bin:$PATH"`

### Import errors
- Make sure you've installed the Python dependencies
- Try running from the project root directory
