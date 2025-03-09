# CBA_Serializer.py

class CBA_Serializer:
    @staticmethod
    def serialize(account_number, account_holder, status, balance):
        """
        Serialize a current bank account record into a fixed-width string using underscores
        as both field separators and padding for alphabetic fields. The format is:
        
            NNNNN_AAAAAAAAAAAAAAAAAAAA_S_PPPPPPPP
        
        where:
          - NNNNN: bank account number, exactly 5 digits (zero-padded)
          - AAAAAAAAAAAAAAAAAAAA: account holder’s name, exactly 20 characters (left-justified, underscore-padded)
          - S: bank account status, exactly 1 character (e.g. 'A' for active or 'D' for disabled)
          - PPPPPPPP: current balance, represented as a 5-digit number (zero-padded) with ".00" appended (8 characters total)
        
        The final string (without the newline) is exactly 37 characters.
        
        Returns:
            A string representing the serialized bank account record (with a newline appended).
        """
        # Format the bank account number: exactly 5 digits, zero-padded.
        account_number_str = str(account_number).zfill(5)
        
        # Format the account holder's name: exactly 20 characters,
        # left-justified and padded with underscores.
        account_holder_str = str(account_holder)[:20].ljust(20, '_')
        
        # Ensure the status is exactly one character.
        status_str = str(status)[0]
        
        # Format the balance: convert to integer dollars (ignoring cents),
        # pad to 5 digits, then append ".00" for an 8-character field.
        balance_str = str(int(balance)).zfill(5) + ".00"
        
        # Combine the fields with underscores as separators.
        serialized_line = f"{account_number_str}_{account_holder_str}_{status_str}_{balance_str}"
        
        # Verify that the line is exactly 37 characters.
        if len(serialized_line) != 37:
            raise ValueError(f"Serialized line is {len(serialized_line)} characters long; expected 37.")
        
        return serialized_line + "\n"
