# Main.py

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
    sample_line = "12345_John_Doe_____________A_00005431\n"
    
    # Create a User (bank account) and load values from the sample line.
    account = User()
    account.load_from_line(sample_line)
    print(account)

    signin()

    # Sample usage of the Parser & Serialization files can go here:
    """
    print("BAT serializer:")
    print(BAT_Serializer.serialize(3, "Mary Smith", 12345, 50.87, ""))
    
    print("CBA serializer:")
    print(CBA_Serializer.serialize(1111, "Steve Mine", "A", 567.00))
    """
