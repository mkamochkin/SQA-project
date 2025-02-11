# Main.py

from User import User
import Transactions

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
 
