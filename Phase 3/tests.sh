#!/bin/bash
# tests.sh - Automated test runner that captures interactive sessions,
# saves console transcripts, and after each test copies the main BAT.txt file
# to the test's output folder, then clears BAT.txt for the next test.
# (Requires Expect installed on your system.)

# Set the project root (assumes this script is one level inside PROJECT_ROOT)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Define the interpreter and the path to your main Python file.
PROGRAM="python3"
PROGRAM_PATH="$PROJECT_ROOT/Phase 2/Phase 2 Code/my_package/Main.py"

# File for current accounts (CBA.txt is used by your program)
CBA_FILE="$PROJECT_ROOT/CBA.txt"

# Permanent BAT file location (the file that accumulates transactions)
BAT_FILE="$PROJECT_ROOT/Phase 3/BAT.txt"

# Define the test categories (should match your folder names under Phase 1/TestCases)
CATEGORIES=(
  #"Login"
  #"Logout"
  #"Withdrawal"
  #"Deposit"
  #"Transfer"
  #"Paybill"
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

  # Determine the input directory (check for "Input" or "input")
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

    # Optionally define a temporary transaction file if your program writes one.
    TEMP_TRANSACTION_FILE="/tmp/${base_name}.atf"

    # Build the command string.
    # Proper quoting ensures paths with spaces are handled correctly.
    COMMAND="$PROGRAM \"$PROGRAM_PATH\" \"$CBA_FILE\" \"$TEMP_TRANSACTION_FILE\""

    # Use an inline Expect script to simulate the interactive session,
    # capturing interleaved input and output into CONSOLE_FILE.
    expect <<EOF
log_file -a "$CONSOLE_FILE"
spawn $COMMAND
# Suppress initial spawn messages.
log_user 0
# Re-enable logging.
log_user 1
set timeout 60
set fp [open "$TEMP_INPUT" r]
while {[gets \$fp line] != -1} {
    send -- "\$line\r"
    send_user "\$line\r"
    sleep 0.5
}
close \$fp
expect eof
EOF

    # Wait a moment (up to 30 seconds) for BAT.txt to have content.
    waited=0
    max_wait=30
    while [ $waited -lt $max_wait ] && [ ! -s "$BAT_FILE" ]; do
      sleep 1
      waited=$((waited+1))
    done

    # Now, after the test run, if the permanent BAT file exists, copy it to the test output folder,
    # then clear (reset) BAT.txt for the next test.
    if [ -f "$BAT_FILE" ]; then
      cp "$BAT_FILE" "$TEST_OUTPUT_DIR/${base_name}_bat.txt"
      > "$BAT_FILE"
    fi

    # Optionally, also handle TEMP_TRANSACTION_FILE if used:
    if [ -f "$TEMP_TRANSACTION_FILE" ]; then
      echo "---- Temp Transaction File ($base_name.atf) ----" >> "$CONSOLE_FILE"
      cat "$TEMP_TRANSACTION_FILE" >> "$CONSOLE_FILE"
      cp "$TEMP_TRANSACTION_FILE" "$TEST_OUTPUT_DIR/$base_name.atf"
      rm -f "$TEMP_TRANSACTION_FILE"
    fi

    echo "==== End of $base_name ====" >> "$CONSOLE_FILE"
    rm -f "$TEMP_INPUT"
  done
done

echo "All tests completed. Check the output folders under $OUTPUT_BASE for full transcripts and BAT files."
