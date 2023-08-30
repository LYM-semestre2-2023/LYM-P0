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
    if len(stack) != 0:
        loque_retorna = False
    return loque_retorna

def agregar_espacios(string:str)-> str:
    a = string.replace("(", " ( ")
    a = a.replace(")", " ) ")
    return a

    
def parser(string:str)->list:
    """
    This function takes a string and returns a list of tokens.
    """
    # Remove all spaces from the string
    # Create a list of tokens
    if not check_cierre_simbolos(string,"(",")"):
        return ["Error: Falta cerrar un paréntesis"]
    if not check_cierre_simbolos(string,"{","}"):
        return ["Error: Falta cerrar una llave"]
    words = re.split("\n|\t|,|\s", string) # Split the string into words
    tokens = []
    variables=[]
    procedures={}
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
            variable=True
            tokens.append("D")
        elif word.lower() == "defproc":
            proc=True
            tokens.append("P")
        elif word=="{":
            tokens.append("{")
        elif word=="}":
            tokens.append("}")
        elif word==";":
            tokens.append(";")

        # Commands
        elif word.lower()=="jump":
            tokens.append("j")
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
        elif word.lower() == "can":
            tokens.append("can")
        elif word.lower() == "not":
            tokens.append("not")
        elif word.lower() == "facing":
            tokens.append("facing")
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
            if variable and word.lower()!="defvar":
                tokens.append(word.lower())
                variables.append(word.lower())
                variable=False
            elif proc and word.lower()!="defproc":
                tokens.append(word.lower())
                procedures[word.lower()]=[]
                proc=False
            elif word.lower() in variables:
                tokens.append(word.lower())
            elif word.lower() in procedures:
                tokens.append(word.lower())
            else:
                if len(word)==1 and word.isalpha():
                    if word.lower() not in procedures[list(procedures.keys())[-1]]:
                        procedures[list(procedures.keys())[-1]].append(word.lower())
                        tokens.append(word.lower())
                    else:
                        tokens.append(word.lower())

        
        # Reinserting parenthesis into tokens
        if left_par:
            tokens.append("(")
        if right_par:
            tokens.append(")")
        

    # Return the list of tokens
    return tokens, variables, procedures

def check_tokens(tokens:list, variables:list, procedures:dict)->bool:
        # Check if the tokens are valid
        while len(tokens)>0:
            token=tokens[0] # Take the first token
            if token=="D" or token=="P": # If it is a definition
                if not check_definitions(tokens, variables, procedures)[0]:
                    return False
                else:
                    tokens=check_definitions(tokens, variables, procedures)[1]
            elif token in ["j","w","l","T","Tt","d","g","gr","lg","nop"]: # If it is a command
                if not check_commands(tokens, variables, procedures)[0]:
                    return False
                else:
                    tokens=check_commands(tokens, variables, procedures)[1]
            elif token in ["if","while","repeat", "else","can","not","facing"]: # If it is a conditional
                if not check_conditionals(tokens, variables, procedures[0]):
                    return False
                else:
                    tokens=check_conditionals(tokens, variables, procedures)[1]     
        return True

def check_definitions(tokens:list, variables:list, procedures:dict)->tuple:
    token=tokens.pop(0)
    if token=="D": # If it is a variable definition
        if tokens.pop(0) not in variables:
            return False, tokens
        if tokens.pop(0)!="#":
            return False, tokens
    elif token=="P": # If it is a procedure definition
        if tokens.pop(0) not in procedures:
            return False, tokens
        else:
            parameters=procedures[tokens.pop(0)]
        if tokens.pop(0)!="(":
            return False, tokens
        while tokens[0]!=")":
            if tokens.pop(0) not in parameters:
                return False, tokens
        tokens.pop(0)
        if tokens.pop(0)!="{":
            return False, tokens
        
        
        
def check_conditionals(tokens:list, variables:list, procedures:dict)->tuple:
    token=tokens.pop(0)
    if token=="if":
        if tokens.pop(0)!="can":
            return False, tokens
        if tokens.pop(0)!="(":
            return False, tokens
        if tokens.pop(0) not in variables:
            return False, tokens
        if tokens.pop(0)!=")":
            return False, tokens
        if tokens.pop(0)!="{":
            return False, tokens
        if not check_commands(tokens, variables, procedures)[0]:
            return False, tokens
        else:
            tokens=check_commands(tokens, variables, procedures)[1]
        if tokens.pop(0)!="}":
            return False, tokens
        if tokens.pop(0)=="else":
            return False, tokens
        if tokens.pop(0)!="{":
            return False, tokens
        if not check_commands(tokens, variables, procedures)[0]:
            return False, tokens
        else:
            tokens=check_commands(tokens, variables, procedures)[1]
        if tokens.pop(0)!="}":
            return False, tokens
        
"""""
def check_commands (tokens, variables, procedures)->tuple:
    token=tokens.pop(0)
    if token=="j":
        if tokens.pop(0)!="(":
            return False, tokens
        if tokens[0] not in variables or tokens[0]!="#":
            return False, tokens
        tokens.pop(0)
        if tokens[0] not in variables or tokens[0]!="#":
            return False, tokens
        tokens.pop(0)
        if tokens.pop(0)!=")":
            return False, tokens
        if tokens.pop(0) not in [";","}"]:
            return False, tokens
    elif token=="w":
    
    elif token=="l":
    
    elif token=="T":
    
    elif token=="Tt":
    elif token=="d":
    elif token=="g":
    elif token=="gr":
    elif token=="lg":
    elif token=="nop":
        if tokens.pop(0)!="(":
            return False, tokens
        if tokens.pop(0)!=")":
            return False, tokens
        if tokens.pop(0) not in [";","}"]:
            return False, tokens
        
"""

#Función que checkea todo el lenguaje de una vez. FALTA agregarle más cosas

def check_lenguage(tokens:list, variables:list, procedures:dict)->bool:
    confirmacion = True
    len_tokens = len(tokens)
    for i in range(0,len_tokens):
        #Checkear declaracion de variables 'D'
        if tokens[i]=='D':
            if tokens[i+1] in variables:
                if tokens[i+2] == "#":
                    confirmacion = True
                else:
                    confirmacion = False
                    print(tokens[i+2])
                    return confirmacion, print("Fallo en la función asdf")
                    
            else:
                confirmacion = False
                return confirmacion, print("Fallo en la función 2")
        #Checkear declaracion de procedimientos 'P'
        elif tokens[i]== 'P':
            if tokens[i+1] in procedures:
                if tokens[i+2] == '(':
                    cantidad_parametros = len(procedures[tokens[i+1]])
                    if cantidad_parametros != 0:
                        for p in range(0,cantidad_parametros):
                            if tokens[i+3+p] in procedures[tokens[i+1]]:
                                confirmacion = True
                            else:
                                confirmacion = False
                                return confirmacion, print("Los parametros no coinciden")
                    if tokens[i+2+cantidad_parametros+1] == ')':
                        confirmacion = True
                    else:
                        confirmacion = False
                        return confirmacion, print("En la declación de parametros no se cierra bien el parentesis")
                    #debido a que se está checkeando al principio que los corchetes si estén bien cerrados sabemos si esto está bien cerrado
                else:
                    confirmacion = False
                    return confirmacion, print("En la declación de parametros no se cierra bien el parentesis")

        #Checkear procedimientos
        elif tokens[i] in procedures:
            len_parametros = len(procedures[tokens[i]])
            if tokens[i+1]=='(':
                if len_parametros!=0:
                    for z in range(0,len_parametros):
                        if tokens[i+2+z] =="#" or tokens[i+2+z] in procedures[tokens[i]]:
                            confirmacion=True
                        else:
                            confirmacion = False
                            print(tokens[i+2+z])
                            return confirmacion, print("El parametro que se ingresó no es númerico, no funciona")
                if tokens[i+1+len_parametros+1] == ')':
                    confirmacion = True
                else:
                    confirmacion = False
                    return confirmacion, print("El procedimiento no tiene un parentesis de cierre bien puesto.")
    print("eso gonorrea, funcionó una retrochimba")
    return confirmacion
            

string="""defVar nom 0
defVar x 0
defVar y 0
defVar one 0
defProc putCB ( c, b )
{
drop ( c ) ;
letGo ( b ) ;
walk ( n )
}
defProc goNorth ()
{
while can( walk ( 1,north )) { walk ( 1,north ) }
}
defProc goWest ()
{
if can( walk ( 1,west )) { walk ( 1,west ) } else nop ()
}
{
jump ( 3,3 ) ;
putCB ( 2,1 )
}"""

valido1="""
{
drop ( 1 ) ;
letGo ( 2 ) ;
walk ( 1 ) ;
while can ( walk ( 1 , north )) {
walk ( 1 , north );
while can ( walk ( 1 , north )) { walk ( 1 , north )}
}
}
"""

valido2="""
defProc putCB ( c , b )
{
drop ( c ) ;
letGo ( b );
walk ( 1 ) ;
putCB ( 1,1 )
}
{
jump ( 3,3 ) ;
putCB ( 2,1 )
}
defProc goNorth ()
{

while can ( walk ( 1 , north )) { walk ( 1 , north ) };
putCB ( 1,1 )

}

{
jump ( 3,4 ) ;
putCB ( 5,5 ) ;
goNorth ()
}

defProc goWest ()
{

if can ( walk ( 1 , west ) ) { walk ( 1 , west )} else { nop () };
goNorth () ;
goWest () ;

}
{
jump ( 4 ,5 ) ;
putCB ( 6 ,7 ) ;
goNorth () ;
goWest () ;
goNorth ()"""

invalido1="""
{
drop () ;
letGo () ;
walk () ;
while can ( walk ( , north ) ) {
walk ( , north );
while can ( walk ( , north ) ) { walk ( , north )
}
}
}"""

invalido2="""
defProc putCB ( c,b )
{
drop ( c ) ;
letGo ( b ) ;
walk ( 1 ) ;
putDC ( 1,1 )
}

{
jump ( 3,3 ) ;
putCB ( 2,1 )
}

defProc goNorth ()
{

while can ( walk ( 1 , north ) ) { walk ( 1 , north ) };
putCB ( 1,1 )

}

{
jump ( 3,4 ) ;
putCB ( 5,5 ) ;
goForth ()
}

defProc goWest ()
{

if can ( walk ( 1 , west ) ) { walk ( 1 , west ) } else { nop () };
goForth () ;
goFest () ;

}

{
jump ( 4,5 ) ;
putCB ( 6,7 ) ;
goNorth () ;
goWest1 () ;
goNorth1 ()
}"""
print(parser(agregar_espacios(string)))