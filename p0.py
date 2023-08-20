import re

def parser(string:str)->list:
    """
    This function takes a string and returns a list of tokens.
    """
    # Remove all spaces from the string
    # Create a list of tokens
    parenthesis=0 #to check if parenthesis are balanced
    for char in string:
        if char=="(":
            parenthesis+=1
        elif char==")":
            parenthesis-=1
    if parenthesis!=0:
        return "Error: Parenthesis not balanced"

    words = re.split(" |\n |\t |,", string.replace("(","").replace(")",""))
    tokens = []
    # Iterate over the string
    for word in words:
        if word.lower() == "defvar":
            tokens.append("D")
        elif word.lower() == "defproc":
            tokens.append("P")
        elif word=="{":
            tokens.append("{")
        elif word=="}":
             tokens.append("}")
        elif word=="(":
             tokens.append("(")
        elif word==")":
             tokens.append(")")
        elif word.isnumeric():
             tokens.append("#")



    # Return the list of tokens
    return tokens   

string=""