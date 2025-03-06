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
       
Author: SQA
Date: [Date]
"""

from User import User
from Transactions import getTransactionInput  # import the transaction input function from Transactions.py
from BAT_Serializer import BAT_Serializer
from CBA_Serializer import CBA_Serializer

backend_path = "ETF.txt"
isAdmin = None

# TODO: For now this returns True always, later add functionality to check if the provided name is valid.
def checkIfValidUser(name):
    return True

def getTypeInput():
    global isAdmin 
    print("Welcome! Please select login type: (standard or admin)")
    typeInput = input().strip().lower()
    
    if typeInput == "standard":
        isAdmin = False
    elif typeInput == "admin":
        isAdmin = True
    else:
        print("Error! Please enter 'standard' or 'admin'")
        getTypeInput()

def signin():
    getTypeInput()

    if not isAdmin:
        print("Standard session type selected. Please enter your name:")
        nameInput = input().strip()
        
        if not checkIfValidUser(nameInput):
            print("This name does not match any user in the database. Please try again.")
            getTypeInput()
        print("Welcome " + nameInput + "!")
        
        print("Please enter which transaction you would like to do:")
        # Listing available transactions for standard users
        print("withdrawal\ntransfer\npaybill\ndeposit\nlogout")
    else:
        print("Welcome admin")
        print("Please enter which transaction you would like to do:")
        # Listing available transactions for admin users
        print("withdrawal\ntransfer\npaybill\ndeposit\ncreate\ndelete\ndisable\nchangeplan\nlogout")

    # Now call the transaction input function from Transactions.py,
    # passing the current session type (isAdmin)
    getTransactionInput(isAdmin)

if __name__ == "__main__":
    # Sample user. Can create multiple users with sample_line1, sample_line2, etc.
    #sample_line = "12345_John_Doe_____________A_00005431\n"
    
    # Create a User (bank account) and load values from the sample line.
    #account = User()
    #account.load_from_line(sample_line)
    #print(account)

    signin()

    # Sample usage of the Parser & Serialization files can go here:
    """
    print("BAT serializer:")
    print(BAT_Serializer.serialize(3, "Mary Smith", 12345, 50.87, ""))
    
    print("CBA serializer:")
    print(CBA_Serializer.serialize(1111, "Steve Mine", "A", 567.00))
    """