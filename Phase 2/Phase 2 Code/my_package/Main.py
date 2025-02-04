# Main.py

from User import User

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
