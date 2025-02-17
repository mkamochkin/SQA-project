# Transactions.py

from User import User
from BAT_Serializer import BAT_Serializer
from CBA_Serializer import CBA_Serializer
from CBA_Parser import CBA_Parser
from BAT_Writer import BAT_Writer
from CBA_Writer import CBA_Writer

# Global dictionary defining which transactions are privileged.
# For standard users, a True value means the transaction is privileged and should be denied.
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

class Transactions:
    def __init__(self, isAdmin):
        # Store the session type so methods know whether to run in admin or standard mode.
        self.isAdmin = isAdmin
        
        self.inputName = ""
        self.inputNumber = 0
        self.amount = 0

        self.accountNumber = None
        self.accountHolderName = None
        self.status = None
        self.balance = None

        self.temp_file = "temp_bat.txt"
        self.perm_file = "BAT.txt"

    # Helper functions for transactions:
    def getName(self):
        #print("What is the account holder's name?")
        self.inputName = input().strip().lower()
        return self.inputName
    
    def getAccountNumber(self):
        #print("What is the account number?")
        self.inputNumber = input().strip()
        return self.inputNumber

    def getRecordLineFromName(self, name):
        """
        Search for a record in "CBA.txt" with a matching account holder's name.
        
        Assumptions:
        - Each record line is fixed-width.
        - The account holder's name is stored in positions 6 to 26.
        - The name field is padded with underscores.
        
        Args:
            name (str): The account holder's name to look for.
            
        Returns:
            str: The matching record line (including newline), or None if not found.
        """
        try:
            with open("CBA.txt", "r") as file:
                for line in file:
                    # Extract the account holder's name field (positions 6 to 26)
                    # Replace underscores with spaces and strip extra whitespace.
                    acct_name_field = line[6:26]
                    acct_name = acct_name_field.replace("_", " ").strip()
                    if acct_name.lower() == name.lower():
                        return line
        except FileNotFoundError:
            print("CBA.txt file not found.")
            return None

        return None
    
    def getRecordLineFromNumber(self, number):
        """
        Search for a record in "CBA.txt" with a matching account number.
        
        Assumptions:
        - Each record line is fixed-width.
        - The account number is stored in the first 5 characters.
        - Account numbers are stored as 5-digit strings.
        
        Args:
            number (int or str): The account number to look for.
            
        Returns:
            str: The matching record line (including newline), or None if not found.
        """
        # Ensure the account number is a 5-digit string.
        number_str = str(number).zfill(5)
        try:
            with open("CBA.txt", "r") as file:
                for line in file:
                    acct_number = line[0:5]
                    if acct_number == number_str:
                        return line
        except FileNotFoundError:
            print("CBA.txt file not found.")
            return None

        return None
        
    def getAmount(self):
        print("Enter the amount:")
        self.amount = input().strip()
        return self.amount
    
    def setVarsFromParserByName(self):
        self.accountNumber, self.accountHolderName, self.status, self.balance = \
            CBA_Parser.parse_line(self.getRecordLineFromName(self.inputName))
    
    def setVarsFromParserByNumber(self):
        self.accountNumber, self.accountHolderName, self.status, self.balance = \
            CBA_Parser.parse_line(self.getRecordLineFromNumber(self.inputNumber))
        
    # Transaction methods:
    def withdraw(self):
        if self.isAdmin:
            print("Enter the source account holder's name:")
            name = self.getName()
            self.setVarsFromParserByName()
            print("How much money do you want to withdraw from " + name + "?")
            amount = self.getAmount()

            if float(amount) > self.balance:
                print("This withdrawal would cause a negative balance. Denied! Try again.")
                self.withdraw()  # Try again
            else:
                BATString = BAT_Serializer.serialize(1, self.accountHolderName, self.accountNumber, amount, "XX")
                # Write the BATString to the temporary file.
                with open(self.temp_file, "a") as temp_file:
                    temp_file.write(BATString)
                CBAString = CBA_Serializer.serialize(self.accountNumber, self.accountHolderName, self.status, self.balance - float(amount))
                CBA_Writer.writeToCBA(CBAString)
                print("Transaction successful!")
                # After finishing, ask for the next transaction.
                getTransactionInput(self.isAdmin)
        else:
            print("Enter your account number:")
            number = self.getAccountNumber()
            self.setVarsFromParserByNumber()
            print("How much money do you want to withdraw?")
            amount = self.getAmount()

            if float(amount) > 500:
                print("Standard users cannot withdraw more than 500. Denied. Try again.")
                self.withdraw()
            elif float(amount) > self.balance:
                print("Withdrawal would cause a negative balance. Denied! Try again.")
                self.withdraw()
            else:
                BATString = BAT_Serializer.serialize(1, self.accountHolderName, self.accountNumber, amount, "XX")
                with open(self.temp_file, "a") as temp_file:
                    temp_file.write(BATString)
                CBAString = CBA_Serializer.serialize(self.accountNumber, self.accountHolderName, self.status, self.balance - float(amount))
                CBA_Writer.writeToCBA(CBAString)
                print("Transaction successful!")
                getTransactionInput(self.isAdmin)

    
    def transfer(self):
        # --- Determine source account details ---
        if self.isAdmin:
            print("Enter the source account holder's name:")
            src_name = self.getName()  # sets self.inputName
            src_line = self.getRecordLineFromName(src_name)
            if src_line is None:
                print("Source account not found for name:", src_name)
                self.transfer()  # Retry
                return
            # Parse the source record line
            src_accountNumber, src_accountHolderName, src_status, src_balance = CBA_Parser.parse_line(src_line)
            print("Enter the source account number:")
            src_input = self.getAccountNumber()  # sets self.inputNumber
            # Compare using zero-padded strings.
            if str(src_accountNumber).zfill(5) != str(src_input).zfill(5):
                print("The source account number does not match the account holder's record. Try again.")
                self.transfer()  # Retry
                return
        else:
            print("Enter your source account number:")
            src_input = self.getAccountNumber()
            src_line = self.getRecordLineFromNumber(src_input)
            if src_line is None:
                print("Source account not found. Try again.")
                self.transfer()  # Retry
                return
            src_accountNumber, src_accountHolderName, src_status, src_balance = CBA_Parser.parse_line(src_line)
        
        # --- Determine destination account details ---
        print("Enter the destination account number:")
        dest_input = self.getAccountNumber()
        dest_line = self.getRecordLineFromNumber(dest_input)
        if dest_line is None:
            print("Destination account not found. Try again.")
            self.transfer()  # Retry
            return
        dest_accountNumber, dest_accountHolderName, dest_status, dest_balance = CBA_Parser.parse_line(dest_line)
        
        # --- Get transfer amount ---
        print("Enter the amount to transfer:")
        transfer_amount_str = self.getAmount()
        try:
            transfer_amount = float(transfer_amount_str)
        except ValueError:
            print("Invalid amount entered. Try again.")
            self.transfer()  # Retry
            return

        # --- Enforce constraints ---
        if not self.isAdmin and transfer_amount > 1000.00:
            print("Standard users cannot transfer more than $1000.00. Try again.")
            self.transfer()  # Retry
            return

        if src_balance - transfer_amount < 0:
            print("Transfer would cause a negative balance in the source account. Denied!")
            self.transfer()  # Retry
            return
        
        # --- Perform the transfer ---
        new_src_balance = src_balance - transfer_amount
        new_dest_balance = dest_balance + transfer_amount

        # Create a BAT record for the transfer. (Transaction code 02 for transfer.)
        BATString = BAT_Serializer.serialize(2, src_accountHolderName, src_accountNumber, transfer_amount_str, "XX")
        with open(self.temp_file, "a") as temp_file:
            temp_file.write(BATString)
        
        # Update the source account in the CBA file.
        new_src_line = CBA_Serializer.serialize(src_accountNumber, src_accountHolderName, src_status, new_src_balance)
        CBA_Writer.writeToCBA(new_src_line)
        
        # Update the destination account in the CBA file.
        new_dest_line = CBA_Serializer.serialize(dest_accountNumber, dest_accountHolderName, dest_status, new_dest_balance)
        CBA_Writer.writeToCBA(new_dest_line)
        
        print("Transfer successful!")
        # After transfer, prompt for the next transaction.
        getTransactionInput(self.isAdmin)


    
    def deposit(self):
        print("Deposit not implemented yet.")
        getTransactionInput(self.isAdmin)

    def delete(self):
        print("Delete not implemented yet.")
        getTransactionInput(self.isAdmin)

    def disable(self):
        print("Disable not implemented yet.")
        getTransactionInput(self.isAdmin)

    def changePlan(self):
        print("Change plan not implemented yet.")
        getTransactionInput(self.isAdmin)

    def paybill(self):
        print("Paybill not implemented yet.")
        getTransactionInput(self.isAdmin)

    def create(self):
        print("Create not implemented yet.")
        getTransactionInput(self.isAdmin)
    
    def logout(self):
        print("Logging out. Processing temporary transactions...")
        # Read the temporary file and write its contents to the permanent file.
        try:
            with open(self.temp_file, "r") as temp_file:
                data = temp_file.read()
            with open(self.perm_file, "a") as perm_file:
                perm_file.write(data)
            print("Transactions have been saved to", self.perm_file)
            # Optionally, clear the temporary file.
            with open(self.temp_file, "w") as temp_file:
                temp_file.write("")
        except FileNotFoundError:
            print("No transactions to process.")
        print("Logged out.")

# Functions to handle transaction input and execution:
def getTransactionInput(isAdmin):
    transactionInput = input("Enter transaction type: ").strip().lower()
    runTransaction(transactionInput, isAdmin)

def runTransaction(transactionInput, isAdmin):
    transaction = Transactions(isAdmin)
    if isAdmin:
        if transactionInput == "withdrawal":
            transaction.withdraw()
        elif transactionInput == "transfer":
            transaction.transfer()
        elif transactionInput == "paybill":
            transaction.paybill()
        elif transactionInput == "deposit":
            transaction.deposit()
        elif transactionInput == "create":
            transaction.create()
        elif transactionInput == "delete":
            transaction.delete()
        elif transactionInput == "disable":
            transaction.disable()
        elif transactionInput == "changeplan":
            transaction.changePlan()
        elif transactionInput == "logout":
            transaction.logout()
        else:
            print("Invalid transaction type. Please try again.")
            getTransactionInput(isAdmin)
    else:
        if transactionInput in isPriviledgedTransaction:
            if isPriviledgedTransaction[transactionInput]:
                print("Privileged transaction denied for standard users. Please select another transaction.")
                getTransactionInput(isAdmin)
            else:
                if transactionInput == "withdrawal":
                    transaction.withdraw()
                elif transactionInput == "transfer":
                    transaction.transfer()
                elif transactionInput == "paybill":
                    transaction.paybill()
                elif transactionInput == "deposit":
                    transaction.deposit()
                elif transactionInput == "logout":
                    transaction.logout()
                else:
                    print("Transaction type not allowed for standard users.")
                    getTransactionInput(isAdmin)
        else:
            print("Invalid transaction type. Please try again.")
            getTransactionInput(isAdmin)
