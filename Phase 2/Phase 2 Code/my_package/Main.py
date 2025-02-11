# Main.py

from User import User

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



if __name__ == "__main__":
    # Input record (37 characters plus newline).
    # Note: Underscores represent spaces in the input.
    sample_line = "12345_John_Doe_____________A_00005431\n"
    
    # Create a User (bank account) and load values from the sample line.
    account = User()
    account.load_from_line(sample_line)
    
    print(account)

    signin()
