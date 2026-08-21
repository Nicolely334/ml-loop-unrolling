#!/usr/bin/env python3
# Extract what LLVM actually decides to unroll

import re
import subprocess
from pathlib import Path
from typing import List, Dict


def extract_llvm_unroll_decisions(source_file: Path, opt_level="O3"):
    """Run clang with -Rpass=loop-unroll to see what LLVM actually does"""
    
    # compile with reporting enabled
    cmd = [
        "clang",
        f"-{opt_level}",
        "-Rpass=loop-unroll",
        "-Rpass-analysis=loop-unroll",
        str(source_file),
        "-o", "/dev/null"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # LLVM prints optimization remarks to stderr
    output = result.stderr
    
    decisions = {
        'unrolled': [],
        'not_unrolled': [],
        'partially_unrolled': []
    }
    
    # parse the remarks
    # Example: "loop-unroll: completely unrolled loop with 4 iterations"
    # Example: "loop-unroll: not unrolling loop, loop body is too large"
    
    for line in output.split('\n'):
        if 'loop-unroll' not in line.lower():
            continue
            
        # try to extract line number
        line_match = re.search(r':(\d+):', line)
        line_num = int(line_match.group(1)) if line_match else None
        
        if 'completely unrolled' in line.lower():
            # extract iteration count if available
            iter_match = re.search(r'(\d+) iterations', line)
            iters = int(iter_match.group(1)) if iter_match else None
            decisions['unrolled'].append({
                'line': line_num,
                'iterations': iters,
                'reason': 'completely unrolled'
            })
            
        elif 'partially unrolled' in line.lower():
            factor_match = re.search(r'factor (\d+)', line)
            factor = int(factor_match.group(1)) if factor_match else None
            decisions['partially_unrolled'].append({
                'line': line_num,
                'factor': factor,
                'reason': 'partial unroll'
            })
            
        elif 'not unrolling' in line.lower() or 'unable to' in line.lower():
            # extract reason
            reason = line.split(':', 2)[-1].strip() if ':' in line else 'unknown'
            decisions['not_unrolled'].append({
                'line': line_num,
                'reason': reason
            })
    
    return decisions


def compare_with_model_predictions(source_file: Path, model_predictions: List[Dict], llvm_decisions: Dict):
    """Compare ML model vs LLVM's actual choices"""
    
    # this is a bit rough since we don't have exact line-to-loop mapping
    # TODO: improve matching between our loop IDs and LLVM line numbers
    
    print(f"\n{'='*60}")
    print(f"Comparison: {source_file.name}")
    print(f"{'='*60}")
    
    total_llvm_unrolled = len(llvm_decisions['unrolled']) + len(llvm_decisions['partially_unrolled'])
    total_llvm_skipped = len(llvm_decisions['not_unrolled'])
    
    print(f"\nLLVM decisions:")
    print(f"  Unrolled: {total_llvm_unrolled}")
    print(f"  Skipped: {total_llvm_skipped}")
    
    print(f"\nOur model predictions:")
    if model_predictions:
        beneficial = sum(1 for p in model_predictions if p.get('beneficial', False))
        print(f"  Predicted beneficial: {beneficial}")
        print(f"  Predicted not beneficial: {len(model_predictions) - beneficial}")
    else:
        print("  (no predictions available)")
    
    # show LLVM's reasoning
    if llvm_decisions['not_unrolled']:
        print(f"\nWhy LLVM didn't unroll:")
        reasons = {}
        for d in llvm_decisions['not_unrolled']:
            r = d['reason']
            reasons[r] = reasons.get(r, 0) + 1
        for reason, count in sorted(reasons.items(), key=lambda x: -x[1]):
            print(f"  - {reason}: {count}x")
    
    print("="*60)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract LLVM's unrolling decisions")
    parser.add_argument("source_file", type=Path)
    parser.add_argument("--opt", default="O3")
    args = parser.parse_args()
    
    print(f"Analyzing {args.source_file.name}...")
    decisions = extract_llvm_unroll_decisions(args.source_file, args.opt)
    
    print(f"\nLLVM Loop Unrolling Decisions:")
    print(f"{'='*60}")
    
    if decisions['unrolled']:
        print(f"\nCompletely unrolled ({len(decisions['unrolled'])}):")
        for d in decisions['unrolled']:
            line_str = f"line {d['line']}" if d['line'] else "unknown line"
            iter_str = f"{d['iterations']} iterations" if d['iterations'] else ""
            print(f"  - {line_str}: {iter_str}")
    
    if decisions['partially_unrolled']:
        print(f"\nPartially unrolled ({len(decisions['partially_unrolled'])}):")
        for d in decisions['partially_unrolled']:
            line_str = f"line {d['line']}" if d['line'] else "unknown line"
            factor_str = f"factor {d['factor']}" if d['factor'] else ""
            print(f"  - {line_str}: {factor_str}")
    
    if decisions['not_unrolled']:
        print(f"\nNot unrolled ({len(decisions['not_unrolled'])}):")
        for d in decisions['not_unrolled'][:5]:  # show first 5
            line_str = f"line {d['line']}" if d['line'] else "unknown line"
            print(f"  - {line_str}: {d['reason']}")
        if len(decisions['not_unrolled']) > 5:
            print(f"  ... and {len(decisions['not_unrolled']) - 5} more")
    
    print("="*60)
    
    return decisions


if __name__ == "__main__":
    main()
