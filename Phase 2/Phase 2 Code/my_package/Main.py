"""
Bank Transaction System Main Program
-------------------------------------

Overall Program Intention:
    This program simulates a simple bank transaction system. It allows users to log in as either
    an admin or a standard user and perform various transactions such as withdrawals, deposits,
    transfers, paying bills, and more. The system updates bank account records and logs transactions
    using fixed-width text files.

Input Files:
    - CBA.txt: A fixed-width text file containing current bank account records.
              Each line represents an account with fields for account number, account holder's name,
              account status, and current balance.
              
Output Files:
    - BAT.txt: A fixed-width text file where finalized transaction records are stored.
    - temp_bat.txt: A temporary file used during a session to store transaction records until logout.
    
How the Program is Intended to be Run:
    1. Ensure that CBA.txt exists in the same directory as the program.
    2. Run the program from the command line using Python 3:
           python Main.py
    3. Follow the on-screen prompts to log in as either an admin or standard user.
    4. Select transactions from the menu as desired. Standard users may have restrictions on certain
       transactions.
    5. When you choose to log out, any transaction data stored in temp_bat.txt is processed and appended
       to BAT.txt.
       
Author: [Your Name]
Date: [Date]
"""

from User import User
from Transactions import Transactions

backend_path = "ETF.txt"
isAdmin = False  # Global variable

# for now this returns True always, later add functionality to test if the name a standard user enters is actually an existing and valid user
def checkIfValidUser(name):
    # In a complete program, add logic to verify if the user exists.
    return True

def signin():
    
    global isAdmin  # Declare isAdmin as global so we can modify it
    print("Welcome! Please select login type: (standard or admin)")
    typeInput = input().strip().lower()

    if typeInput == "standard":
        isAdmin = False
    elif typeInput == "admin":
        isAdmin = True
    else:
        print("Error! Please enter 'standard' or 'admin'")
        return  # Optionally exit the function if input is invalid

    if not isAdmin:
        print("Standard session type selected. Please enter your name:")
        nameInput = input().strip()
        print("name: " + nameInput)
        
        if not checkIfValidUser:
            print("This name does not match up with a user in the database. Please try again.")

        # load in data from database text file by user name
        # path to file is in var backend_path
    else:
        print("Welcome admin")

    
    #dictionary that holds the transactions and whether
    # True if priviledged
    isPriviledgedTransaction = {
        "delete" : True,
        "disable" : True,
        "create" : True,
        "withdraw" : False,
        "paybill" : False,
        "deposit" : False,
        "transfer" : False,
        "changePlan" : False,
    }

    def allowtransaction():
        
        if (isAdmin == False):
            print('Standard session type selected. Welcome name.\n Select transaction:')
            


if __name__ == "__main__":
    # Input record (37 characters plus newline).
    # Note: Underscores represent spaces in the input.
    sample_line = "12345_John_Doe_____________A_00005431\n"
    
    # Create a User (bank account) and load values from the sample line.
    account = User()
    account.load_from_line(sample_line)
    
    print(account)
    # Expected output:
    # BankAccount(account_number=12345, account_holder='John Doe', status=A, balance=5431.0)

    # Proceed with the interactive sign-in process using standard input.
    signin()
    # promt to enter transaction type
    # asdasd()

    """
    if not isAdmin:
        if transactionDict[desiredTranscation] == True
        print ("You don't have the permissions for this")
        else (desiredTransaction())
    """





