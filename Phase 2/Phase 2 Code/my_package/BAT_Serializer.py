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
          - AAAAAAAAAAAAAAAAAAA: account holder’s name, exactly 19 characters,
            left-justified, with any spaces replaced by underscores and padded with underscores.
          - NNNNN: bank account number, exactly 5 digits (zero-padded)
          - PPPPPPPP: amount, a 5-digit number (zero-padded) with ".00" appended 
            (8 characters total)
          - MM: miscellaneous info, exactly 2 characters, left-justified,
            with any spaces replaced by underscores and padded with underscores.

        The final string (without the newline) must be exactly 40 characters.

        Returns:
            A string representing the serialized transaction record (with a newline appended).
        """
        # Format the transaction code: 2 digits, zero-padded.
        trans_code_str = str(transaction_code).zfill(2)
        
        # Format the account holder's name:
        # Replace any spaces with underscores, truncate to 19 characters,
        # then left-justify and pad with underscores to exactly 19 characters.
        account_holder_str = str(account_holder)[:19].replace(" ", "_").ljust(19, '_')
        
        # Format the account number: exactly 5 digits, zero-padded.
        account_number_str = str(account_number).zfill(5)
        
        # Format the amount:
        # Convert to float then to an integer (ignoring cents),
        # pad it to 5 digits with zeros, and append ".00" to create an 8-character field.
        amount_str = str(int(float(amount))).zfill(5) + ".00"
        
        # Format the miscellaneous field:
        # Replace any spaces with underscores, truncate to 2 characters,
        # then left-justify and pad with underscores to exactly 2 characters.
        misc_str = str(misc)[:2].replace(" ", "_").ljust(2, '_')
        
        # Combine the fields with underscores as separators.
        serialized_line = f"{trans_code_str}_{account_holder_str}_{account_number_str}_{amount_str}_{misc_str}"
        
        # Verify that the line is exactly 40 characters.
        if len(serialized_line) != 40:
            raise ValueError(f"Serialized line is {len(serialized_line)} characters long; expected 40.")
        
        return serialized_line + "\n"
