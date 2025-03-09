#!/bin/bash
##############################################################################
# run_all_tests_to_single_file.sh
#
# This script loops over each category folder in:
#   SQA-project/Phase 1/TestCases/<Category>/
# and for each .txt file in the "Input/" subfolder, runs your Main.py program,
# capturing the console output into ONE file: "Phase 3/output.txt".
#
# Directory assumptions:
#   1) This script is in: SQA/SQA-project/Phase 3/
#   2) "Main.py" is at:   SQA/SQA-project/Phase 2/Phase 2 Code/my_package/Main.py
#   3) "CBA.txt" is at:   SQA/SQA-project/CBA.txt
#   4) Each category folder under "Phase 1/TestCases" has an "Input" (or "input")
#      subfolder containing .txt test files.
#
# Usage:
#   1) cd SQA/SQA-project/Phase 3
#   2) chmod +x run_all_tests_to_single_file.sh
#   3) ./run_all_tests_to_single_file.sh
##############################################################################

# --------------------- Locate the "project root" ---------------------------
# If this script is inside "SQA/SQA-project/Phase 3", going one level up
# should give us "SQA/SQA-project".
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# --------------------- Python program path (using python3) -----------------
#   If "python3" is not found, install it (sudo apt-get install python3)
#   or adjust to the exact path (e.g., /usr/bin/python3).
#
#   Notice "Phase 2 Code" has spaces, so we put the path in quotes.
PROGRAM="python3 \"$PROJECT_ROOT/Phase 2/Phase 2 Code/my_package/Main.py\""

# Path to your main current bank accounts file
CBA_FILE="$PROJECT_ROOT/CBA.txt"

# We'll store everything in a single output file under Phase 3
COMBINED_OUTPUT_FILE="$PROJECT_ROOT/Phase 3/output.txt"

# --------------------- Define the categories (subfolders) ------------------
CATEGORIES=(
  "Login"
  "Logout"
  "Withdrawal"
  "Deposit"
  "Transfer"
  "Paybill"
  "Create"
  "Delete"
  "Disable"
  "changeplan"
)

# --------------------- Begin script logic ----------------------------------

# Start/clear the combined output file
echo "==== ALL TEST RUNS ($(date)) ====" > "$COMBINED_OUTPUT_FILE"

# For each category, we look for Phase 1/TestCases/<Category>/Input/*.txt
for category in "${CATEGORIES[@]}"; do
  
  CATEGORY_DIR="$PROJECT_ROOT/Phase 1/TestCases/$category"

  # Some folders use "Input", others "input". We'll check "Input" first.
  if [ -d "$CATEGORY_DIR/Input" ]; then
    INPUT_DIR="$CATEGORY_DIR/Input"
  else
    INPUT_DIR="$CATEGORY_DIR/input"
  fi

  # If there's no input dir, skip
  if [ ! -d "$INPUT_DIR" ]; then
    echo "[Skipping] No input folder found for category '$category' at $INPUT_DIR." >> "$COMBINED_OUTPUT_FILE"
    continue
  fi

  echo "" >> "$COMBINED_OUTPUT_FILE"
  echo "----------------------------------------" >> "$COMBINED_OUTPUT_FILE"
  echo "CATEGORY: $category" >> "$COMBINED_OUTPUT_FILE"
  echo "----------------------------------------" >> "$COMBINED_OUTPUT_FILE"

  # Loop over each .txt input file
  for input_file in "$INPUT_DIR"/*.txt; do
    # Skip if none found
    [ -f "$input_file" ] || continue

    # Extract something like "TC_login_01" from "TC_login_01.txt"
    base_name="$(basename "$input_file")"
    test_name="${base_name%.txt}"

    echo "" >> "$COMBINED_OUTPUT_FILE"
    echo "==== Running $test_name ====" >> "$COMBINED_OUTPUT_FILE"

    # Temporary transaction file path for this run
    TEMP_TRANSACTION_FILE="/tmp/${test_name}.atf"

    # Run the program, capturing both stdout and stderr
    # We pass 2 arguments: (CBA_FILE, TEMP_TRANSACTION_FILE)
    # and feed input_file to stdin.
    console_output=$(
      eval $PROGRAM "\"$CBA_FILE\"" "\"$TEMP_TRANSACTION_FILE\"" < "$input_file" 2>&1
    )

    # Append the console output to the combined file
    echo "$console_output" >> "$COMBINED_OUTPUT_FILE"

    # If you want to also show what was written to the transaction file,
    # do so here:
    if [ -f "$TEMP_TRANSACTION_FILE" ]; then
      echo "---- Transaction File ($test_name.atf) ----" >> "$COMBINED_OUTPUT_FILE"
      cat "$TEMP_TRANSACTION_FILE" >> "$COMBINED_OUTPUT_FILE"
      rm -f "$TEMP_TRANSACTION_FILE"  # Remove if not needed
    fi

    echo "==== End of $test_name ====" >> "$COMBINED_OUTPUT_FILE"
    echo "" >> "$COMBINED_OUTPUT_FILE"
  done

done

echo "All tests completed. Consolidated output is in: $COMBINED_OUTPUT_FILE"
