# User.py

from CBA_Parser import CBA_Parser

class User:
    def __init__(self):
        self.account_number = None
        self.account_holder = None
        self.status = None
        self.balance = None

    def load_from_line(self, record_line: str):
        """
        Load the bank account data by parsing the fixed-width record line.
        """
        acct_num, holder, stat, bal = CBA_Parser.parse_line(record_line)
        self.account_number = acct_num
        self.account_holder = holder
        self.status = stat
        self.balance = bal

    def __str__(self):
        return (
            f"BankAccount("
            f"account_number={self.account_number}, "
            f"account_holder='{self.account_holder}', "
            f"status={self.status}, "
            f"balance={self.balance})"
        )
