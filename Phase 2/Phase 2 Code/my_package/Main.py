#!/usr/bin/env python3
import sys
from User import User
import Transactions

# Global variable to track login type.
isAdmin = False

def checkIfValidUser(name):
    # In a complete program, add logic to verify if the user exists.
    return True

def signin():
    global isAdmin
    print("Welcome! Please select login type: (standard or admin)")
    typeInput = input().strip().lower()

    if typeInput == "standard":
        isAdmin = False
    elif typeInput == "admin":
        isAdmin = True
    else:
        print("Error! Please enter 'standard' or 'admin'")
        return

    if not isAdmin:
        print("Standard session type selected. Please enter your name:")
        nameInput = input().strip()
        print("name: " + nameInput)
        if not checkIfValidUser(nameInput):
            print("This name does not match any user in the database. Please try again.")
    else:
        print("Welcome admin")

if __name__ == "__main__":
    # Ensure that exactly two command-line arguments (besides the script name) are provided.
    if len(sys.argv) != 3:
        print("Usage: bank-atm <current accounts file> <transaction output file>")
        sys.exit(1)

    current_accounts_file = sys.argv[1]
    transaction_output_file = sys.argv[2]

    # Read bank account records from the input file.
    accounts = []
    try:
        with open(current_accounts_file, 'r') as infile:
            for line in infile:
                if line.strip() == "":
                    continue  # Skip empty lines.
                try:
                    user = User()
                    user.load_from_line(line)
                    accounts.append(user)
                except Exception as e:
                    print(f"Error processing line: {line.strip()} - {e}")
    except FileNotFoundError:
        print(f"Error: The file {current_accounts_file} does not exist.")
        sys.exit(1)

    # Log the loaded accounts to standard output.
    print("Loaded bank accounts:")
    for account in accounts:
        print(account)

    # Proceed with the interactive sign-in process using standard input.
    signin()

    # (Placeholder) Process transactions here.
    # In a complete program, you would handle the transaction type and update account data accordingly.
    transaction_log = "Transaction log output placeholder"

    # Write the transaction log to the specified output file.
    try:
        with open(transaction_output_file, 'w') as outfile:
            outfile.write(transaction_log)
    except Exception as e:
        print(f"Error writing to output file {transaction_output_file}: {e}")
