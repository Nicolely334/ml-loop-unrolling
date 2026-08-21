#!/usr/bin/env python3
"""
Make predictions on new programs using the trained model.
"""

import argparse
import pickle
import sys
from pathlib import Path

import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from compile_and_measure import BenchmarkRunner
from parse_llvm_ir import extract_features_from_ir


def load_model(model_path: Path, scaler_path: Path):
    """Load the trained model and scaler."""
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    
    return model, scaler


def predict_unrolling_benefit(source_file: Path, model, scaler, runner: BenchmarkRunner):
    """
    Predict whether loop unrolling will benefit a program.

    Args:
        source_file: Path to C source file
        model: Trained ML model
        scaler: Fitted StandardScaler
        runner: BenchmarkRunner instance

    Returns:
        Dictionary with predictions and probabilities
    """
    # Compile to LLVM IR
    print(f"\nAnalyzing: {source_file.name}")
    print("-" * 60)
    
    ir_file = runner.compile_to_llvm_ir(source_file, opt_level="O0")
    print(f"✓ Compiled to IR: {ir_file}")
    
    # Extract features
    loop_features = extract_features_from_ir(ir_file)
    
    if not loop_features:
        print("⚠️  No loops detected")
        return None
    
    print(f"✓ Found {len(loop_features)} loop(s)")
    
    # Prepare features
    feature_columns = [
        'num_instructions',
        'num_basic_blocks',
        'num_load_instructions',
        'num_store_instructions',
        'num_branches',
        'num_calls',
        'num_arithmetic_ops',
        'estimated_trip_count',
        'has_constant_trip_count',
        'nesting_depth',
        'num_phi_nodes',
        'num_memory_dependencies',
        'has_early_exit',
        'num_exits',
    ]
    
    results = []
    
    for idx, features in enumerate(loop_features):
        # Create feature vector
        X = pd.DataFrame([features])[feature_columns]
        
        # Handle missing values
        X['estimated_trip_count'] = X['estimated_trip_count'].replace(-1, 1000000)
        
        # Scale features (only if model requires it)
        try:
            X_scaled = scaler.transform(X)
            prediction = model.predict(X_scaled)[0]
            
            # Get probability if available
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(X_scaled)[0]
                confidence = proba[prediction]
            else:
                confidence = None
        except:
            # If scaling fails, try without scaling (for tree-based models)
            prediction = model.predict(X)[0]
            
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(X)[0]
                confidence = proba[prediction]
            else:
                confidence = None
        
        result = {
            'loop_id': features['loop_id'],
            'prediction': 'Beneficial' if prediction == 1 else 'Not Beneficial',
            'confidence': confidence,
            'features': features,
        }
        
        results.append(result)
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Predict loop unrolling benefit using trained ML model"
    )
    parser.add_argument("source_file", type=Path, help="C source file to analyze")
    parser.add_argument(
        "--model",
        type=Path,
        default=Path(__file__).parent.parent / "models" / "best_model.pkl",
        help="Path to trained model",
    )
    parser.add_argument(
        "--scaler",
        type=Path,
        default=Path(__file__).parent.parent / "models" / "scaler.pkl",
        help="Path to fitted scaler",
    )
    
    args = parser.parse_args()
    
    # Check if model exists
    if not args.model.exists():
        print(f"❌ Model not found: {args.model}")
        print("\nTrain a model first:")
        print("  1. Collect data: python src/collect_dataset.py")
        print("  2. Train models: jupyter notebook notebooks/02_train_models.ipynb")
        return 1
    
    # Load model
    print("Loading model...")
    model, scaler = load_model(args.model, args.scaler)
    print(f"✓ Model loaded from: {args.model}")
    
    # Initialize runner
    runner = BenchmarkRunner(opt_level="O3")
    
    # Make predictions
    predictions = predict_unrolling_benefit(args.source_file, model, scaler, runner)
    
    if not predictions:
        return 1
    
    # Display results
    print("\n" + "=" * 60)
    print("Predictions")
    print("=" * 60)
    
    for pred in predictions:
        print(f"\nLoop: {pred['loop_id']}")
        print(f"  Prediction: {pred['prediction']}")
        
        if pred['confidence'] is not None:
            print(f"  Confidence: {pred['confidence']:.1%}")
        
        print(f"\n  Loop characteristics:")
        print(f"    Instructions: {pred['features']['num_instructions']}")
        print(f"    Trip count: {pred['features']['estimated_trip_count']}")
        print(f"    Memory ops: {pred['features']['num_memory_dependencies']}")
        print(f"    Branches: {pred['features']['num_branches']}")
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    beneficial_count = sum(1 for p in predictions if p['prediction'] == 'Beneficial')
    print(f"Total loops: {len(predictions)}")
    print(f"Predicted beneficial: {beneficial_count}")
    print(f"Predicted not beneficial: {len(predictions) - beneficial_count}")
    
    if beneficial_count > 0:
        print(f"\n✓ Recommendation: Use -funroll-loops")
    else:
        print(f"\n✓ Recommendation: Use -fno-unroll-loops")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
