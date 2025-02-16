# BAT_Serializer.py

class BAT_Serializer:
    @staticmethod
    def serialize(transaction_code, account_holder, account_number, amount, misc):
        """
        Serialize a bank account transaction record into a fixed-width string using underscores
        as separators. The format is:
        
            CC_AAAAAAAAAAAAAAAAAAA_NNNNN_PPPPPPPP_MM

        where:
          - CC: 2-digit transaction code (zero-padded)
          - AAAAAAAAAAAAAAAAAAA: account holder’s name, exactly 19 characters, left-justified, underscore-padded
          - NNNNN: bank account number, exactly 5 digits (zero-padded)
          - PPPPPPPP: amount, a 5-digit number (zero-padded) with ".00" appended (8 characters total)
          - MM: miscellaneous info, exactly 2 characters, left-justified, underscore-padded

        The final string (without the newline) must be exactly 40 characters.

        Returns:
            A string representing the serialized transaction record (with a newline appended).
        """
        # Format the transaction code: 2 digits, zero-padded.
        trans_code_str = str(transaction_code).zfill(2)
        
        # Format the account holder's name: exactly 19 characters,
        # left-justified and padded with underscores.
        account_holder_str = str(account_holder)[:19].ljust(19, '_')
        
        # Format the account number: exactly 5 digits, zero-padded.
        account_number_str = str(account_number).zfill(5)
        
        # Format the amount: convert to integer dollars (ignoring cents),
        # pad to 5 digits, then append ".00" for an 8-character field.
        amount_str = str(float(amount)).zfill(5) + ".00"
        
        # Format the miscellaneous field: exactly 2 characters, left-justified, underscore-padded.
        misc_str = str(misc)[:2].ljust(2, '_')
        
        # Combine the fields with underscores as separators.
        serialized_line = f"{trans_code_str}_{account_holder_str}_{account_number_str}_{amount_str}_{misc_str}"
        
        # Verify that the line is exactly 40 characters.
        if len(serialized_line) != 40:
            raise ValueError(f"Serialized line is {len(serialized_line)} characters long; expected 40.")
        
        return serialized_line + "\n"
