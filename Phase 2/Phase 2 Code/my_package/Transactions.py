from User import User
from BAT_Serializer import BAT_Serializer
from CBA_Serializer import CBA_Serializer
from CBA_Parser import CBA_Parser
from BAT_Writer import BAT_Writer
from CBA_Writer import CBA_Writer

class Transactions:
    def __init__(self):
        self.inputName = ""
        self.inputNumber = 0
        self.amount = 0

        self.accountNumber = None
        self.accountHolderName = None
        self.status = None
        self.balance = None

        self.BATList = []

    # Helper functions for transactions:
    
    def getName(self):
        self.inputName = input().strip().lower()
        return self.inputName
    
    def getAccountNumber(self):
        self.inputNumber = input()
        return self.inputNumber

    def getRecordLineFromName(self, name):
        return "12345_John_Doe_____________A_00005431\n"
    
    def getRecordLineFromNumber(number):
        return "22222_Bill_Hat_____________A_00009932\n"
    
    def getAmount(self):
        self.amount = input()
        return self.amount
    
    def setVarsFromParserByName(self):
        self.accountNumber, self.accountHolderName, self.status, self.balance = CBA_Parser.parse_line(self.getRecordLineFromName(self.inputName))
        return

    def setVarsFromParserByNumber(self):
        self.accountNumber, self.accountHolderName, self.status, self.balance = CBA_Parser.parse_line(self.getRecordLineFromNumber(self.inputNumber))
        return
        
    
    # Transactions:
    def withdraw(self, isAdmin):
        if isAdmin:
            print("What is the account holder's name?")
            name = self.getName()
            self.setVarsFromParserByName()
            print("How much money do you want to withdraw from " + name + "?")
            amount = self.getAmount()

            if int(amount) > self.balance:
                print ("This user will have a negative amount after this withdrawal. Denied!")
            else:
                BATString =  BAT_Serializer.serialize(1, self.accountHolderName, self.accountNumber, amount, "XX")
                self.BATList.append(BATString)
                CBAString = CBA_Serializer.serialize(self.accountNumber, self.accountHolderName, self.status, self.balance - int(amount))
                CBA_Writer.writeToCBA(CBAString)
        else:
            print("What is the account number?")

    def deposit(self):
        # Deposit logic here.
        return

    def delete(self):
        # Delete logic here.
        return

    def disable(self):
        # Disable logic here.
        return

    def changePlan(self):
        # Change plan logic here.
        return

    def transfer(self):
        # Transfer logic here.
        return

    def paybill(self):
        # Pay bill logic here.
        return

    def create(self):
        # Create logic here.
        return
    
    def logout(self):
        for BAT in self.BATList:
            BAT_Writer.writeToBAT(BAT)
        return
