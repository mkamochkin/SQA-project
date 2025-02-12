# Main.py

from User import User
from Transactions import Transactions
from BAT_Serializer import BAT_Serializer
from CBA_Serializer import CBA_Serializer

# TODO: Currently we don't read any bank info from a text file, it's done manually through sample strings. Add functionality to read from file(s). 
backend_path = "ETF.txt"
isAdmin = None
transactionInput = ""

# Global dictionary holding the transactions and whether they are privileged.
# True means the transaction is privileged (and should be denied for standard users).
isPriviledgedTransaction = {
    "delete": True,
    "disable": True,
    "create": True,
    "withdrawal": False,
    "paybill": False,
    "deposit": False,
    "transfer": False,
    "changeplan": True,
    "logout": False
}

# TODO: For now this returns True always, later add functionality to check if the provided name is valid.
def checkIfValidUser(name):
    return True

# This method gets input and calls that transaction
# Use this instead of creating an input every time
def getTransactionInput():
    transactionInput = input().strip().lower()
    runTransaction(transactionInput)
    
# This method determines if the user is allowed to run the transaction, if allowed call that transaction
# If not allowed, try again
# TODO: Right now this loops indefinitely until a valid input is entered, add functionality to get out of this loop

def runTransaction(transactionInput):
    if isAdmin:
        # Admin users can perform all transactions.
        if transactionInput == "withdrawal":
            Transactions.withdraw()
        elif transactionInput == "transfer":
            Transactions.transfer()
        elif transactionInput == "paybill":
            Transactions.paybill()
        elif transactionInput == "deposit":
            Transactions.deposit()
        elif transactionInput == "create":
            Transactions.create()
        elif transactionInput == "delete":
            Transactions.delete()
        elif transactionInput == "disable":
            Transactions.disable()
        elif transactionInput == "changeplan":
            Transactions.changePlan()
        elif transactionInput == "logout":
            Transactions.logout()
        else:
            print("Invalid transaction type. Please try again.")
    else:
        # For standard users, first check if the transaction type is defined.
        if transactionInput in isPriviledgedTransaction:
            # If the transaction is privileged, deny it.
            if isPriviledgedTransaction[transactionInput]:
                print("Privileged transaction denied for standard users. Please select another transaction")
                # Try again
                getTransactionInput()
            else:
                # Otherwise, execute the corresponding transaction.
                if transactionInput == "withdrawal":
                    Transactions.withdraw()
                elif transactionInput == "transfer":
                    Transactions.transfer()
                elif transactionInput == "paybill":
                    Transactions.paybill()
                elif transactionInput == "deposit":
                    Transactions.deposit()
                elif transactionInput == "logout":
                    Transactions.logout()
                else:
                    # In case the transaction type is defined in the dictionary but not allowed for standard users.
                    print("Transaction type not allowed for standard users.")
        else:
            print("Invalid transaction type. Please try again.")
            # Try again
            getTransactionInput()

# This method gets session type input (admin or standard)
# TODO: This loops indefinitely until a valid input is entered. Add functionality to get out of this loop.
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

# Functionality of signin():
# prompts to enter session type
# prompts to enter name (if standard)
# greets user
# gets transaction input
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
        # TODO: this looks ugly in console.
        print("withdrawal\ntransfer\npaybill\ndeposit\nlogout")
    else:
        print("Welcome admin")
        print("Please enter which transaction you would like to do:")
        # TODO: this looks ugly in console.
        print("withdrawal\ntransfer\npaybill\ndeposit\ncreate\ndelete\ndisable\nchangeplan\nlogout")


    getTransactionInput()

    
if __name__ == "__main__":
    
    # Sample user. Can create multiple users with sample_line1, sample_line2, etc. 
    sample_line = "12345_John_Doe_____________A_00005431\n"
    
    # Create a User (bank account) and load values from the sample line.
    # Same thing here; can create multiple accounts with account1 = User, account2 = User, etc. 
    account = User()
    account.load_from_line(sample_line)
    print(account)

    signin()
    
    # Sample usage of the 3 Parser & Serialization files to use in Transactions.py:
    """
    print("BAT serializer:")
    print(BAT_Serializer.serialize(3, "Mary Smith", 12345, 50.87, ""))
    
    print("CBA serializer:")
    print(CBA_Serializer.serialize(1111, "Steve Mine", "A", 567.00))
    """