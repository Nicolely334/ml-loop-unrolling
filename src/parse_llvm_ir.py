#!/usr/bin/env python3

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class LoopFeatures:
    loop_id: str
    num_instructions: int
    num_basic_blocks: int
    num_load_instructions: int
    num_store_instructions: int
    num_branches: int
    num_calls: int
    num_arithmetic_ops: int
    estimated_trip_count: Optional[int]
    has_constant_trip_count: bool
    nesting_depth: int
    num_phi_nodes: int
    num_memory_dependencies: int
    has_early_exit: bool
    num_exits: int
    
    def to_dict(self):
        return {
            'loop_id': self.loop_id,
            'num_instructions': self.num_instructions,
            'num_basic_blocks': self.num_basic_blocks,
            'num_load_instructions': self.num_load_instructions,
            'num_store_instructions': self.num_store_instructions,
            'num_branches': self.num_branches,
            'num_calls': self.num_calls,
            'num_arithmetic_ops': self.num_arithmetic_ops,
            'estimated_trip_count': self.estimated_trip_count or -1,
            'has_constant_trip_count': int(self.has_constant_trip_count),
            'nesting_depth': self.nesting_depth,
            'num_phi_nodes': self.num_phi_nodes,
            'num_memory_dependencies': self.num_memory_dependencies,
            'has_early_exit': int(self.has_early_exit),
            'num_exits': self.num_exits,
        }


class LLVMIRParser:
    def __init__(self, ir_file: Path):
        self.ir_file = ir_file
        self.ir_content = self._read_ir()

    def _read_ir(self):
        if not self.ir_file.exists():
            raise FileNotFoundError(f"IR file not found: {self.ir_file}")
        return self.ir_file.read_text()

    def get_loop_info_from_opt(self):
        try:
            result = subprocess.run(
                ["opt", "-passes=loop-simplify,loop-rotate,loop(print)",
                 "-disable-output", str(self.ir_file)],
                capture_output=True,
                text=True,
                check=False,
            )

            loops = []
            for match in re.finditer(r"Loop at depth (\d+) containing:", result.stderr):
                loops.append({"depth": int(match.group(1))})
            return loops
        except FileNotFoundError:
            # opt not available, fall back to manual parsing
            return []

    def extract_basic_features(self, basic_block_content: str):
        features = {
            'num_instructions': 0,
            'num_load': 0,
            'num_store': 0,
            'num_branches': 0,
            'num_calls': 0,
            'num_arithmetic': 0,
            'num_phi': 0,
        }

        for line in basic_block_content.split('\n'):
            line = line.strip()
            if not line or line.startswith(';'):
                continue

            features['num_instructions'] += 1
            if 'load' in line: features['num_load'] += 1
            if 'store' in line: features['num_store'] += 1
            if 'br ' in line: features['num_branches'] += 1
            if 'call' in line: features['num_calls'] += 1
            if any(op in line for op in ['add ', 'sub ', 'mul ', 'div ', 'fadd', 'fsub', 'fmul', 'fdiv']):
                features['num_arithmetic'] += 1
            if 'phi ' in line: features['num_phi'] += 1

        return features

    def find_loops_simple(self) -> List[LoopFeatures]:
        """
        Simple heuristic loop detection from LLVM IR.
        Looks for basic blocks with back edges (branches to earlier blocks).

        Returns:
            List of LoopFeatures objects
        """
        loops = []
        
        # Split IR into functions
        functions = re.split(r'define.*?\{', self.ir_content)
        
        for func_idx, func_content in enumerate(functions[1:], 1):  # Skip preamble
            # Find basic blocks
            bb_pattern = r'^(\w+):\s*;.*?(?=^\w+:|^})'
            blocks = re.findall(bb_pattern, func_content, re.MULTILINE | re.DOTALL)
            
            if not blocks:
                continue

            # Look for loops (simplified: find blocks with backward branches)
            for bb_idx, (bb_name, bb_content) in enumerate(blocks):
                # Check if this block branches to itself or earlier blocks
                br_matches = re.findall(r'br.*?label %(\w+)', bb_content)
                
                has_backedge = False
                for target in br_matches:
                    # Check if target is this block or an earlier one
                    target_blocks = [b[0] for b in blocks[:bb_idx+1]]
                    if target in target_blocks:
                        has_backedge = True
                        break

                if has_backedge:
                    # Extract features for this potential loop
                    features_dict = self.extract_basic_features(bb_content)
                    
                    # Try to estimate trip count from comparison instructions
                    trip_count = self._estimate_trip_count(bb_content)
                    
                    loop_features = LoopFeatures(
                        loop_id=f"func{func_idx}_bb{bb_idx}_{bb_name}",
                        num_instructions=features_dict['num_instructions'],
                        num_basic_blocks=1,  # Simplified
                        num_load_instructions=features_dict['num_load'],
                        num_store_instructions=features_dict['num_store'],
                        num_branches=features_dict['num_branches'],
                        num_calls=features_dict['num_calls'],
                        num_arithmetic_ops=features_dict['num_arithmetic'],
                        estimated_trip_count=trip_count,
                        has_constant_trip_count=trip_count is not None,
                        nesting_depth=1,  # Simplified
                        num_phi_nodes=features_dict['num_phi'],
                        num_memory_dependencies=features_dict['num_load'] + features_dict['num_store'],
                        has_early_exit=features_dict['num_branches'] > 1,
                        num_exits=features_dict['num_branches'],
                    )
                    
                    loops.append(loop_features)

        return loops

    def _estimate_trip_count(self, bb_content: str) -> Optional[int]:
        """
        Attempt to estimate loop trip count from comparison instructions.

        Args:
            bb_content: Basic block content

        Returns:
            Estimated trip count if detectable, else None
        """
        # Look for patterns like: icmp slt i64 %i, 100000000
        cmp_pattern = r'icmp.*?(\d+)'
        matches = re.findall(cmp_pattern, bb_content)
        
        if matches:
            try:
                return int(matches[0])
            except ValueError:
                pass
        
        return None

    def get_all_loop_features(self) -> List[LoopFeatures]:
        """
        Extract features for all loops in the IR file.

        Returns:
            List of LoopFeatures objects
        """
        # Try opt-based analysis first
        opt_loops = self.get_loop_info_from_opt()
        
        # Fall back to simple heuristic parsing
        if not opt_loops:
            return self.find_loops_simple()
        
        # Combine opt info with manual feature extraction
        return self.find_loops_simple()


def extract_features_from_ir(ir_file: Path) -> List[Dict]:
    """
    Convenience function to extract all loop features from an IR file.

    Args:
        ir_file: Path to .ll file

    Returns:
        List of feature dictionaries
    """
    parser = LLVMIRParser(ir_file)
    loop_features = parser.get_all_loop_features()
    return [lf.to_dict() for lf in loop_features]


def main():
    """Example usage."""
    import argparse
    import pandas as pd

    parser = argparse.ArgumentParser(description="Extract loop features from LLVM IR")
    parser.add_argument("ir_file", type=Path, help="LLVM IR file (.ll)")
    parser.add_argument("--output", type=Path, help="Output CSV file (optional)")

    args = parser.parse_args()

    print(f"Parsing LLVM IR: {args.ir_file}")
    features = extract_features_from_ir(args.ir_file)

    if not features:
        print("No loops detected in the IR file.")
        return

    df = pd.DataFrame(features)
    print(f"\nFound {len(df)} loop(s):")
    print(df.to_string())

    if args.output:
        df.to_csv(args.output, index=False)
        print(f"\nFeatures saved to: {args.output}")


if __name__ == "__main__":
    main()
