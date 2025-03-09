#!/bin/bash
# run_tests.sh
# This script automates running your Python project on each test input file.

# Directories
INPUT_DIR="/mnt/c/SQA project/SQA-project/Phase 1/TestCases/deposit/input"
OUTPUT_DIR="/mnt/c/SQA project/SQA-project/Phase 1/TestCases/deposit/output"

# Ensure the output directory exists.
mkdir -p "$OUTPUT_DIR"

# Change into the working directory that contains your project files.
# This directory must contain Main.py, CBA.txt, BAT.txt, etc.
cd "/mnt/c/SQA project/SQA-project/Phase 2/Phase 2 Code/my_package" || exit

# Loop over each test file in the input directory.
for testfile in "$INPUT_DIR"/*.txt; do
    base=$(basename "$testfile" .txt)
    echo "Running test $base"
    # Run your project using your command-line arguments.
    # Here we run the project with CBA.txt and BAT.txt (which are in the current directory).
    # The test file is redirected as input, and the terminal output is saved to an output file.
    python3 Main.py CBA.txt BAT.txt < "$testfile" > "$OUTPUT_DIR/${base}.out"
    
    # Optionally, if your project writes the transaction output to BAT.txt,
    # you might copy it for each test run:
    cp BAT.txt "$OUTPUT_DIR/${base}.txt"
    # And then clear BAT.txt if necessary before the next run.
    > BAT.txt
done

echo "All tests completed."
