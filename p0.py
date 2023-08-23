import re

def check_cierre_simbolos(string_largo:str,simbolo_apertura:str, simbolo_cierre:str)->bool:
    #Esta función checkea si los simbolos están abiertos y cerrados correctamente:
    # Ej: () bien cerrado
    # Ej: )() mal cerrado
    stack = []
    loque_retorna = True
    for i in string_largo:
        if i == simbolo_apertura:
            stack.append(0)
        elif i == simbolo_cierre and len(stack)>=1:
            stack.pop()
        elif i == simbolo_cierre and len(stack) ==0:
            loque_retorna = False
    return loque_retorna
    
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
        return ["Error: Parenthesis not balanced"]

    words = re.split(" |\n |\t |,", string)
    tokens = []
    # Iterate over the string
    for word in words: 
        # Conditions to check if parenthesis are present
        left_par=False
        right_par=False

        # Elmiminating parenthesis from the word
        if "(" in word:
            left_par=True
            word=word.replace("(","")
        if ")" in word:
            right_par=True
            word=word.replace(")","")
        # Converting each word to its assigned token

        # Definitions
        if word.lower() == "defvar":
            tokens.append("D")
        elif word.lower() == "defproc":
            tokens.append("P")
        elif word=="{":
            tokens.append("{")
        elif word=="}":
             tokens.append("}")

        # Commands
        elif word.lower()=="walk":
            tokens.append("w")
        elif word.lower()=="leap":
            tokens.append("l")
        elif word.lower()=="turn":
            tokens.append("T")
        elif word.lower()=="turnto":
            tokens.append("Tt")
        elif word.lower()=="drop":
            tokens.append("d")
        elif word.lower()=="get":
            tokens.append("g")
        elif word.lower()=="grab":
            tokens.append("gr")
        elif word.lower()=="letgo":
            tokens.append("lg")
        elif word.lower()=="nop":
            tokens.append("nop")

        
        # Conditionals
        elif word.lower() == "if":
             tokens.append("if")
        elif word.lower() == "else":
            tokens.append("else")
        elif word.lower() == "while":
            tokens.append("while")
        elif word.lower() == "repeat":
            tokens.append("repeat")
        elif word.lower() == "times":
            tokens.append("times")

        # Numbers
        elif word.isnumeric():
             tokens.append("#")

        
        
        # Cardinal Directions
        elif word.lower() == "north":
            tokens.append("N")
        elif word.lower() == "south":
            tokens.append("S")
        elif word.lower() == "east":
            tokens.append("E")
        elif word.lower() == "west":
            tokens.append("W")

        # Directions
        elif word.lower() == "front":
            tokens.append("F")
        elif word.lower() == "back":
            tokens.append("B")
        elif word.lower() == "left":
            tokens.append("L")
        elif word.lower() == "right":
            tokens.append("R")
        elif word.lower() == "around":
            tokens.append("A")
        
        
        # Names
        else:
            tokens.append("Name")
        
        # Reinserting parenthesis into tokens
        if right_par:
            tokens.append(")")
        if left_par:
            tokens.append("(")



    # Return the list of tokens
    return tokens   

string=""