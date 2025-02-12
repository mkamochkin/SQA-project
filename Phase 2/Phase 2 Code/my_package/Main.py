# Main.py

from User import User
from Transactions import Transactions
from BAT_Serializer import BAT_Serializer
from CBA_Serializer import CBA_Serializer

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

    
    sample_line = "12345_John_Doe_____________A_00005431\n"
    
    # Create a User (bank account) and load values from the sample line.
    account = User()
    account.load_from_line(sample_line)

    signin()
 
    """   
    print("CBA Parser:")
    print(account)

    print("BAT serializer:")
    print(BAT_Serializer.serialize(3, "Mary Smith", 12345, 50.87, ""))

    print("CBA serializer:")
    print(CBA_Serializer.serialize(1111, "Steve Mine", "A", 567.00))
    """

    
    
    
    # promt to enter transaction type
    # asdasd()

    """
    if not isAdmin:
        if transactionDict[desiredTranscation] == True
        print ("You don't have the permissions for this")
        else (desiredTransaction())
    """





