#!/usr/bin/env python3
"""
Verify that the project setup is correct.
"""

import sys
from pathlib import Path


def check_python_version():
    """Check Python version."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor}.{version.micro} (need 3.9+)")
        return False


def check_dependencies():
    """Check if required Python packages are installed."""
    print("\nChecking Python dependencies...")
    required = [
        'numpy',
        'pandas',
        'sklearn',
        'matplotlib',
        'seaborn',
        'jupyter',
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (not installed)")
            missing.append(package)
    
    return len(missing) == 0


def check_llvm_tools():
    """Check if LLVM tools are available."""
    print("\nChecking LLVM tools...")
    import subprocess
    
    tools = ['clang', 'opt']
    available = []
    
    for tool in tools:
        try:
            result = subprocess.run(
                [tool, '--version'],
                capture_output=True,
                text=True,
                check=True
            )
            version_line = result.stdout.splitlines()[0]
            print(f"  ✓ {tool}: {version_line}")
            available.append(tool)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"  ✗ {tool} (not found)")
    
    return len(available) == len(tools)


def check_project_structure():
    """Check that project structure is correct."""
    print("\nChecking project structure...")
    
    required_paths = [
        'src/compile_and_measure.py',
        'src/parse_llvm_ir.py',
        'src/__init__.py',
        'benchmarks/simple_loop.c',
        'notebooks/01_pipeline_validation.ipynb',
        'pyproject.toml',
        'requirements.txt',
    ]
    
    project_root = Path(__file__).parent
    all_exist = True
    
    for path_str in required_paths:
        path = project_root / path_str
        if path.exists():
            print(f"  ✓ {path_str}")
        else:
            print(f"  ✗ {path_str} (missing)")
            all_exist = False
    
    return all_exist


def check_src_imports():
    """Check if src modules can be imported."""
    print("\nChecking src module imports...")
    
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root / 'src'))
    
    try:
        from compile_and_measure import BenchmarkRunner
        print("  ✓ compile_and_measure.BenchmarkRunner")
    except ImportError as e:
        print(f"  ✗ compile_and_measure.BenchmarkRunner: {e}")
        return False
    
    try:
        from parse_llvm_ir import LLVMIRParser
        print("  ✓ parse_llvm_ir.LLVMIRParser")
    except ImportError as e:
        print(f"  ✗ parse_llvm_ir.LLVMIRParser: {e}")
        return False
    
    return True


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("ML Loop Unrolling Project - Setup Verification")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Python Dependencies", check_dependencies),
        ("LLVM Tools", check_llvm_tools),
        ("Project Structure", check_project_structure),
        ("Module Imports", check_src_imports),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\nError during {name} check: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        symbol = "✓" if passed else "✗"
        print(f"  {symbol} {name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All checks passed! You're ready to go.")
        print("\nNext steps:")
        print("  1. Run: python src/compile_and_measure.py benchmarks/simple_loop.c")
        print("  2. Open: jupyter notebook notebooks/01_pipeline_validation.ipynb")
    else:
        print("\n⚠️  Some checks failed. Please review the output above.")
        print("\nTo fix:")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Install LLVM: See SETUP.md for instructions")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
