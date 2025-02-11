# Main.py

from User import User
    
backend_path = "ETF.txt"

def signin():
    
    isAdmin = False
    print("Welcome! Please select login type: (standard or admin)")
    typeInput = input()
    if (typeInput == "standard"):
        isAdmin = False
    elif (typeInput == "admin"):
        isAdmin = True
    else: (print("Error! Please enter 'standard' or 'admin'"))

    if (isAdmin == False):
        print("Standard session type seleted. Please enter your name:")
        nameInput = input()
        print("name:" + nameInput)
    else (isAdmin == True):
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
    # Expected output:
    # BankAccount(account_number=12345, account_holder='John Doe', status=A, balance=5431.0)

