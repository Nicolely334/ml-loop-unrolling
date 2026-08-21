#!/usr/bin/env python3
# quick baseline - this was the first attempt with binary classification
# (see notebooks/04_regression_model.ipynb for the better approach)

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

dataset_path = Path(__file__).parent.parent / 'data' / 'processed' / 'dataset.csv'
df = pd.read_csv(dataset_path)

print(f"Dataset: {len(df)} loops")
print(f"  Beneficial: {df['beneficial'].sum()} ({df['beneficial'].mean()*100:.1f}%)")
print(f"  Not beneficial: {(1-df['beneficial']).sum()} ({(1-df['beneficial']).mean()*100:.1f}%)")
print()

# features
feature_columns = [
    'num_instructions', 'num_basic_blocks', 'num_load_instructions',
    'num_store_instructions', 'num_branches', 'num_calls', 'num_arithmetic_ops',
    'estimated_trip_count', 'has_constant_trip_count', 'nesting_depth',
    'num_phi_nodes', 'num_memory_dependencies', 'has_early_exit', 'num_exits'
]

X = df[feature_columns].copy()
y = df['beneficial'].copy()

# handle -1 trip counts
X['estimated_trip_count'] = X['estimated_trip_count'].replace(-1, 1000000)

# split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y if len(df) > 10 else None
)

print(f"Train: {len(X_train)}, Test: {len(X_test)}")
print()

# scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# train models
models = {
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
    'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=5),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10),
}

print("="*60)
print("Model Performance")
print("="*60)

for name, model in models.items():
    if 'Logistic' in name:
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    print(f"\n{name}:")
    print(f"  Accuracy:  {acc:.3f}")
    print(f"  Precision: {prec:.3f}")
    print(f"  Recall:    {rec:.3f}")
    print(f"  F1-Score:  {f1:.3f}")
    
    # feature importance for tree models
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        top_features = sorted(zip(feature_columns, importances), key=lambda x: -x[1])[:5]
        print(f"  Top features:")
        for feat, imp in top_features:
            print(f"    {feat}: {imp:.3f}")

print("\n" + "="*60)
