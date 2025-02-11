# Main.py

from User import User
import Transactions

backend_path = "ETF.txt"
isAdmin = False  # Global variable

# for now this returns True always, later add functionality to test if the name a standard user enters is actually an existing and valid user
def checkIfValidUser(name):
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

    
    #dictionary that holds the transactions
    transactionDict = {
        Transactions.delete : 1,
        Transactions.disable : 2,
        Transactions.withdraw : 3,
        Transactions.paybill: 4,
        Transactions.deposit: 5,
        Transactions.transfer: 6,
        Transactions.changePlan: 7,
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

    signin()

