
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"


PROGRAM="python3 \"$PROJECT_ROOT/Phase 2/Phase 2 Code/my_package/Main.py\""


CBA_FILE="$PROJECT_ROOT/CBA.txt"


COMBINED_OUTPUT_FILE="$PROJECT_ROOT/Phase 3/output.txt"


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


echo "==== ALL TEST RUNS ($(date)) ====" > "$COMBINED_OUTPUT_FILE"


for category in "${CATEGORIES[@]}"; do
  
  CATEGORY_DIR="$PROJECT_ROOT/Phase 1/TestCases/$category"


  if [ -d "$CATEGORY_DIR/Input" ]; then
    INPUT_DIR="$CATEGORY_DIR/Input"
  else
    INPUT_DIR="$CATEGORY_DIR/input"
  fi


  if [ ! -d "$INPUT_DIR" ]; then
    echo "[Skipping] No input folder found for category '$category' at $INPUT_DIR." >> "$COMBINED_OUTPUT_FILE"
    continue
  fi

  echo "" >> "$COMBINED_OUTPUT_FILE"
  echo "----------------------------------------" >> "$COMBINED_OUTPUT_FILE"
  echo "CATEGORY: $category" >> "$COMBINED_OUTPUT_FILE"
  echo "----------------------------------------" >> "$COMBINED_OUTPUT_FILE"


  for input_file in "$INPUT_DIR"/*.txt; do
    [ -f "$input_file" ] || continue
    base_name="$(basename "$input_file")"
    test_name="${base_name%.txt}"

    echo "" >> "$COMBINED_OUTPUT_FILE"
    echo "==== Running $test_name ====" >> "$COMBINED_OUTPUT_FILE"


    TEMP_TRANSACTION_FILE="/tmp/${test_name}.atf"

    console_output=$(
      eval $PROGRAM "\"$CBA_FILE\"" "\"$TEMP_TRANSACTION_FILE\"" < "$input_file" 2>&1
    )

    echo "$console_output" >> "$COMBINED_OUTPUT_FILE"

    if [ -f "$TEMP_TRANSACTION_FILE" ]; then
      echo "---- Transaction File ($test_name.atf) ----" >> "$COMBINED_OUTPUT_FILE"
      cat "$TEMP_TRANSACTION_FILE" >> "$COMBINED_OUTPUT_FILE"
      rm -f "$TEMP_TRANSACTION_FILE" 
    fi

    echo "==== End of $test_name ====" >> "$COMBINED_OUTPUT_FILE"
    echo "" >> "$COMBINED_OUTPUT_FILE"
  done

done

echo "All tests completed. Consolidated output is in: $COMBINED_OUTPUT_FILE"
