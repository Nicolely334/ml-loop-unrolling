.PHONY: help install verify collect train predict clean

help:
	@echo "ML Loop Unrolling Project - Make Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install       Install Python dependencies"
	@echo "  make verify        Verify setup is correct"
	@echo ""
	@echo "Workflow:"
	@echo "  make collect       Collect dataset from benchmarks"
	@echo "  make train         Open training notebook"
	@echo "  make predict       Run prediction on example program"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean         Clean generated files"
	@echo "  make test-single   Test pipeline on single benchmark"

install:
	pip install -r requirements.txt
	@echo "✓ Dependencies installed"

verify:
	python verify_setup.py

collect:
	python src/collect_dataset.py --runs 20 --warmup 5
	@echo ""
	@echo "✓ Dataset collected to: data/processed/dataset.csv"

train:
	jupyter notebook notebooks/02_train_models.ipynb

predict:
	@echo "Example prediction:"
	python src/predict.py benchmarks/small_loop.c

test-single:
	@echo "Testing pipeline on simple_loop.c..."
	python src/compile_and_measure.py benchmarks/simple_loop.c --runs 10

clean:
	@echo "Cleaning generated files..."
	find benchmarks -name "*.ll" -delete
	find benchmarks -name "*_unroll" -delete
	find benchmarks -name "*_no_unroll" -delete
	rm -f benchmarks/*.out
	rm -rf data/raw/*.json data/raw/*.csv
	rm -rf __pycache__ src/__pycache__
	@echo "✓ Cleaned"

workflow:
	@echo "Complete workflow:"
	@echo ""
	@echo "1. make install     # Install dependencies"
	@echo "2. make verify      # Check setup"
	@echo "3. make collect     # Collect dataset (5-10 min)"
	@echo "4. make train       # Train models (open notebook)"
	@echo "5. make predict     # Test prediction"
