#!/usr/bin/env python3
# Compare our ML predictions against what LLVM actually does

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from compile_and_measure import BenchmarkRunner
from parse_llvm_ir import extract_features_from_ir
from extract_llvm_decisions import extract_llvm_unroll_decisions


def analyze_program(source_file: Path, opt_level="O3"):
    """Run both our model's feature extraction and LLVM's decisions"""
    
    print(f"\n{'='*70}")
    print(f"Analyzing: {source_file.name}")
    print(f"{'='*70}")
    
    runner = BenchmarkRunner(opt_level=opt_level)
    
    # get our features
    print("\n[1/2] Extracting features from IR...")
    ir_file = runner.compile_to_llvm_ir(source_file, opt_level="0")
    our_features = extract_features_from_ir(ir_file)
    
    # get LLVM's decisions
    print("[2/2] Extracting LLVM's decisions...")
    llvm_decisions = extract_llvm_unroll_decisions(source_file, opt_level)
    
    return our_features, llvm_decisions


def print_comparison(source_file: Path, our_features, llvm_decisions):
    """Print side-by-side comparison"""
    
    print(f"\n{'Results':^70}")
    print("="*70)
    
    # our analysis
    print("\nOur feature analysis:")
    if our_features:
        for feat in our_features:
            print(f"  Loop {feat['loop_id']}:")
            print(f"    Instructions: {feat['num_instructions']}")
            print(f"    Trip count: {feat['estimated_trip_count']}")
            print(f"    Memory ops: {feat['num_memory_dependencies']}")
    else:
        print("  (no loops detected)")
    
    # LLVM's decisions
    total_unrolled = len(llvm_decisions['unrolled']) + len(llvm_decisions['partially_unrolled'])
    total_skipped = len(llvm_decisions['not_unrolled'])
    
    print(f"\nLLVM's decisions:")
    print(f"  Unrolled: {total_unrolled}")
    print(f"  Not unrolled: {total_skipped}")
    
    if llvm_decisions['unrolled']:
        print(f"\n  Completely unrolled loops:")
        for d in llvm_decisions['unrolled']:
            iters = f"{d['iterations']} iters" if d['iterations'] else "unknown count"
            print(f"    - {iters}")
    
    if llvm_decisions['not_unrolled']:
        print(f"\n  Why loops weren't unrolled:")
        # group by reason
        reasons = {}
        for d in llvm_decisions['not_unrolled']:
            r = d['reason']
            reasons[r] = reasons.get(r, 0) + 1
        
        for reason, count in sorted(reasons.items(), key=lambda x: -x[1])[:3]:
            print(f"    - {reason} ({count}x)")
    
    print("="*70)


def batch_compare(benchmarks_dir: Path, opt_level="O3"):
    """Compare all benchmarks"""
    
    source_files = sorted(benchmarks_dir.glob("*.c"))
    
    results = []
    
    for source_file in source_files:
        try:
            our_features, llvm_decisions = analyze_program(source_file, opt_level)
            print_comparison(source_file, our_features, llvm_decisions)
            
            results.append({
                'file': source_file.name,
                'our_loops': len(our_features),
                'llvm_unrolled': len(llvm_decisions['unrolled']) + len(llvm_decisions['partially_unrolled']),
                'llvm_skipped': len(llvm_decisions['not_unrolled']),
            })
        except Exception as e:
            print(f"\n❌ Error processing {source_file.name}: {e}")
            continue
    
    # summary table
    print(f"\n\n{'='*70}")
    print(f"{'Summary Across All Benchmarks':^70}")
    print(f"{'='*70}")
    print(f"{'File':<30} {'Our Loops':<12} {'LLVM Unrolled':<15} {'LLVM Skipped':<15}")
    print("-"*70)
    
    for r in results:
        print(f"{r['file']:<30} {r['our_loops']:<12} {r['llvm_unrolled']:<15} {r['llvm_skipped']:<15}")
    
    print("="*70)
    
    # aggregate stats
    total_our = sum(r['our_loops'] for r in results)
    total_llvm_unrolled = sum(r['llvm_unrolled'] for r in results)
    total_llvm_skipped = sum(r['llvm_skipped'] for r in results)
    
    print(f"\nTotals:")
    print(f"  Our loop detection: {total_our} loops")
    print(f"  LLVM unrolled: {total_llvm_unrolled}")
    print(f"  LLVM skipped: {total_llvm_skipped}")
    
    if total_our > 0:
        # FIXME: this comparison is rough because our loop detection != LLVM's
        # need better matching between our loop IDs and LLVM's decisions
        print(f"\nNote: Direct comparison is approximate - our loop detection")
        print(f"      uses heuristics while LLVM has full loop analysis")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Compare ML features vs LLVM decisions")
    parser.add_argument("--file", type=Path, help="Single file to analyze")
    parser.add_argument("--benchmarks", type=Path, 
                       default=Path(__file__).parent.parent / "benchmarks",
                       help="Benchmark directory for batch analysis")
    parser.add_argument("--opt", default="O3")
    
    args = parser.parse_args()
    
    if args.file:
        our_features, llvm_decisions = analyze_program(args.file, args.opt)
        print_comparison(args.file, our_features, llvm_decisions)
    else:
        batch_compare(args.benchmarks, args.opt)


if __name__ == "__main__":
    main()
