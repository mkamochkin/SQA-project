#!/bin/bash
# tests.sh - Automated test runner using inline Expect to capture full interactive sessions
# with interleaved input and output, and organizing outputs by test case.
# (Requires Expect installed on your system.)

# Set the project root (assumes this script is one level inside PROJECT_ROOT)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Define the interpreter and the path to your main Python file.
PROGRAM="python3"
PROGRAM_PATH="$PROJECT_ROOT/Phase 2/Phase 2 Code/my_package/Main.py"

# File for current accounts (CBA.txt)
CBA_FILE="$PROJECT_ROOT/CBA.txt"

# Define the test categories (should match your folder names under Phase 1/TestCases)
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

# Base output directory for test results (for example, under Phase 3)
OUTPUT_BASE="$PROJECT_ROOT/Phase 3"

# Loop through each test category.
for category in "${CATEGORIES[@]}"; do
  CATEGORY_DIR="$PROJECT_ROOT/Phase 1/TestCases/$category"

  # Determine the input directory (check for either "Input" or "input").
  if [ -d "$CATEGORY_DIR/Input" ]; then
    INPUT_DIR="$CATEGORY_DIR/Input"
  else
    INPUT_DIR="$CATEGORY_DIR/input"
  fi

  if [ ! -d "$INPUT_DIR" ]; then
    echo "[Skipping] No input folder found for category '$category' at $INPUT_DIR."
    continue
  fi

  # Create the parent output folder for this category (e.g., Deposit_TestOutput)
  CATEGORY_OUTPUT_DIR="$OUTPUT_BASE/${category}_TestOutput"
  mkdir -p "$CATEGORY_OUTPUT_DIR"

  # Loop over each test input file in the input directory.
  for input_file in "$INPUT_DIR"/*.txt; do
    [ -f "$input_file" ] || continue
    base_name="$(basename "$input_file" .txt)"
    # Create an output folder for this test case (e.g., TC_Deposit_01_TestOutput)
    TEST_OUTPUT_DIR="$CATEGORY_OUTPUT_DIR/${base_name}_TestOutput"
    mkdir -p "$TEST_OUTPUT_DIR"

    # File to store the full transcript (interleaved input and output)
    CONSOLE_FILE="$TEST_OUTPUT_DIR/console.txt"
    echo "==== Running $base_name ($(date)) ====" > "$CONSOLE_FILE"

    # Create a temporary input file that appends "logout" if not already present.
    TEMP_INPUT="/tmp/${base_name}_input.txt"
    cp "$input_file" "$TEMP_INPUT"
    last_line=$(tail -n 1 "$TEMP_INPUT" | tr '[:upper:]' '[:lower:]')
    if [ "$last_line" != "logout" ]; then
      echo "logout" >> "$TEMP_INPUT"
    fi

    # Define a temporary transaction (BAT) file for this test run.
    TEMP_TRANSACTION_FILE="/tmp/${base_name}.atf"

    # Build the command string.
    # Using proper quoting for paths with spaces.
    COMMAND="$PROGRAM \"$PROGRAM_PATH\" \"$CBA_FILE\" \"$TEMP_TRANSACTION_FILE\""

    # Use an inline Expect script to drive the interactive session.
    expect <<EOF
# Log everything to the specified file.
log_file -a "$CONSOLE_FILE"
# Spawn the command. (The spawn line will be logged by default.)
spawn $COMMAND
# Immediately disable logging to hide the spawn message.
log_user 0
# Now re-enable logging.
log_user 1
set timeout 60
# Open the temporary input file.
set fp [open "$TEMP_INPUT" r]
while {[gets \$fp line] != -1} {
    send -- "\$line\r"
    sleep 0.5
}
close \$fp
expect eof
EOF

    # If the temporary transaction file exists, append its contents to the transcript and copy it.
    if [ -f "$TEMP_TRANSACTION_FILE" ]; then
      echo "---- Transaction File ($base_name.atf) ----" >> "$CONSOLE_FILE"
      cat "$TEMP_TRANSACTION_FILE" >> "$CONSOLE_FILE"
      cp "$TEMP_TRANSACTION_FILE" "$TEST_OUTPUT_DIR/$base_name.atf"
      rm -f "$TEMP_TRANSACTION_FILE"
    fi

    echo "==== End of $base_name ====" >> "$CONSOLE_FILE"
    rm -f "$TEMP_INPUT"
  done
done

echo "All tests completed. Check the output folders under $OUTPUT_BASE for full transcripts and BAT files."
