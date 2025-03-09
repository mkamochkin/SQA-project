# CBA_Writer.py

class CBA_Writer:
    @staticmethod
    def writeToCBA(new_line):
        """
        Writes a new CBA record line to CBA.txt by updating the existing record 
        for the same account number. If no matching record exists, the new line is appended.

        Args:
            new_line (str): The new CBA record line (should be exactly 37 characters, plus newline)
        """
        filename = "CBA.txt"
        
        # Ensure new_line ends with a newline
        if not new_line.endswith("\n"):
            new_line += "\n"
        
        # Extract the account number from the new line (first 5 characters)
        new_acc_num = new_line[:5]
        
        try:
            with open(filename, "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            # If the file doesn't exist, create a new list
            lines = []
        
        found = False
        # Loop through existing lines to find a matching account number
        for i in range(len(lines)):
            # Compare the first 5 characters (account number)
            if lines[i][:5] == new_acc_num:
                # Overwrite the existing line with the new line
                lines[i] = new_line
                found = True
                break
        
        # If no matching record was found, append the new line.
        if not found:
            lines.append(new_line)
        
        # Write all lines back to the file (overwriting the file)
        with open(filename, "w") as file:
            file.writelines(lines)
