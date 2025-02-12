#CBa_Parser.py

class CBA_Parser:
    @staticmethod
    def parse_line(record_line: str):
        """
        Parse a 37-character fixed-width bank record line in the form:
            NNNNN_AAAAAAAAAAAAAAAAAAAA_S_PPPPPPPP

        Where underscores represent spaces. The fields are:
            - NNNNN: bank account number (right-justified, zero-padded)
            - AAAAAAAAAAAAAAAAAAAA: account holder's name (left-justified, space-padded)
            - S: account status ('A' for active, 'D' for disabled)
            - PPPPPPPP: current balance (numeric value with .00 appended)

        Returns:
            A tuple: (account_number, account_holder, status, balance)
        """
        # Remove the trailing newline (if any)
        record_line = record_line.rstrip('\n')
        
        # Validate that the record line is exactly 37 characters
        if len(record_line) != 37:
            raise ValueError("Record line must be exactly 37 characters long.")
        
        # Field slicing based on the fixed-width positions:
        #   0-4   : account number (5 characters)
        #   5     : separator (an underscore representing a space)
        #   6-25  : account holder's name (20 characters, underscores represent spaces)
        #   26    : separator (underscore)
        #   27    : account status (1 character)
        #   28    : separator (underscore)
        #   29-36 : balance (8 characters)
        account_num_str = record_line[0:5]
        name_str        = record_line[6:26]
        status          = record_line[27]
        balance_str     = record_line[29:37]

        # Convert the fields:
        account_num = int(account_num_str)
        # Replace underscores with spaces then strip any trailing spaces.
        account_holder = name_str.replace('_', ' ').rstrip()
        balance = float(balance_str)

        return account_num, account_holder, status, balance
