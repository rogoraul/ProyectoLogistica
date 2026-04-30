#!/bin/bash

echo "Starting full experimental pipeline..."

echo "1/6: Running calibration..."
python3 experiments/calibration.py

echo "2/6: Running comparison..."
python3 experiments/comparison.py

echo "3/6: Generating Excel files..."
python3 experiments/generate_excel.py

echo "4/6: Running main script (ts_evolution + convergence_data)..."
python3 main.py

echo "5/6: Running time analysis - 180s convergence curves..."
python3 experiments/time_analysis.py

echo "6/6: Executing Jupyter Notebook..."
if command -v jupyter &> /dev/null; then
    jupyter nbconvert --to notebook --execute --inplace notebooks/visualize_csvs.ipynb
else
    echo "jupyter command not found. Trying with python3 -m jupyter..."
    python3 -m jupyter nbconvert --to notebook --execute --inplace notebooks/visualize_csvs.ipynb
fi

echo "Pipeline completed successfully!"
