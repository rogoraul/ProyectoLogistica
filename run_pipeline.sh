#!/bin/bash

echo "Starting full experimental pipeline..."

echo "1/5: Running calibration..."
python3 experiments/calibration.py

echo "2/5: Running comparison..."
python3 experiments/comparison.py

echo "3/5: Generating Excel files..."
python3 experiments/generate_excel.py

echo "4/5: Running main script..."
python3 main.py

echo "5/5: Executing Jupyter Notebook..."
if command -v jupyter &> /dev/null; then
    jupyter nbconvert --to notebook --execute --inplace notebooks/visualize_csvs.ipynb
else
    echo "jupyter command not found. Trying with python3 -m jupyter..."
    python3 -m jupyter nbconvert --to notebook --execute --inplace notebooks/visualize_csvs.ipynb
fi

echo "Pipeline completed successfully!"
