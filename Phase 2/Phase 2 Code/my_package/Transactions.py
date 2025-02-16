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
        print("What is the account holder's name?")
        self.inputName = input().strip().lower()
        return self.inputName
    
    def getAccountNumber(self):
        print("What is the account number?")
        self.inputNumber = input().strip()
        return self.inputNumber

    def getRecordLineFromName(self, name):
        # In a real application, retrieve the correct record line for this name.
        return "12345_John_Doe_____________A_00005431\n"
    
    def getRecordLineFromNumber(self, number):
        # In a real application, retrieve the correct record line for this account number.
        return "22222_Bill_Hat_____________A_00009932\n"
    
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

    def transfer(self):
        print("Transfer not implemented yet.")
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
