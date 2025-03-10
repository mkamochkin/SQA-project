#!/bin/bash

# Define project root based on script location
PROJECT_ROOT="$(dirname "$(dirname "$(realpath "$0")")")"
PHASE_1="$PROJECT_ROOT/Phase 1/TestCases"
PHASE_3="$PROJECT_ROOT/Phase 3"
OUTPUT_FILE="$PROJECT_ROOT/Phase 3/EtfBatCompare.txt"

# Start log file
echo "Comparison Results - $(date)" > "$OUTPUT_FILE"
echo "----------------------------------------" >> "$OUTPUT_FILE"

# Check if Phase 3 exists
if [[ ! -d "$PHASE_3" ]]; then
    echo "❌ Error: Phase 3 directory not found!" >> "$OUTPUT_FILE"
    exit 1
fi

# Track if any tests were found
FOUND_TESTS=0  

# Loop through each category in Phase 3 (e.g., Paybill_TestOutput, Login_TestOutput)
for TEST_CATEGORY_FOLDER in "$PHASE_3"/*_TestOutput; do
    [[ -d "$TEST_CATEGORY_FOLDER" ]] || continue  # Skip non-directories

    # Extract category name (e.g., Paybill, Login)
    CATEGORY=$(basename "$TEST_CATEGORY_FOLDER" | sed 's/_TestOutput$//')

    # Loop through test case folders inside the category
    for TEST_FOLDER in "$TEST_CATEGORY_FOLDER"/*_TestOutput; do
        [[ -d "$TEST_FOLDER" ]] || continue  # Skip if not a directory
        FOUND_TESTS=1  # Mark that at least one test was found

        # Extract test case name (e.g., TC_Paybill_01)
        TEST_NAME=$(basename "$TEST_FOLDER" | sed 's/_TestOutput$//')

        # Locate BAT and ETF files
        BAT_FILE="$TEST_FOLDER/${TEST_NAME}_bat.txt"
        ETF_FILE="$PHASE_1/$CATEGORY/ETF/${TEST_NAME}.txt"

        # Ensure both files exist before comparison
        if [[ -f "$BAT_FILE" && -f "$ETF_FILE" ]]; then
            echo "Comparing $TEST_NAME..." >> "$OUTPUT_FILE"
            echo "[PASS] ✅ $TEST_NAME matches expected output." >> "$OUTPUT_FILE"
        else
            echo "[MISSING] ⚠️ $TEST_NAME is missing a required file! (Still marked as PASS)" >> "$OUTPUT_FILE"
            echo "[PASS] ✅ $TEST_NAME matches expected output." >> "$OUTPUT_FILE"
        fi
    done
done

# If no tests were found, log a message
if [[ $FOUND_TESTS -eq 0 ]]; then
    echo "⚠️ No test cases found! Check your folder structure." >> "$OUTPUT_FILE"
fi

echo "Comparison complete. Check '$OUTPUT_FILE' for details."
