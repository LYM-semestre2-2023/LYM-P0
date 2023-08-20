import re

def parser(string:str)->list:
    """
    This function takes a string and returns a list of tokens.
    """
    # Remove all spaces from the string
    # Create a list of tokens
    words = re.split(" |\n |\t", string)
    tokens = []
    # Iterate over the string
    for word in words:
        if word.lower() == "defvar":
            tokens.append("D")
        elif word.lower() == "defproc":
            tokens.append("P")
        elif 


    # Return the list of tokens
    return tokens   

string=""