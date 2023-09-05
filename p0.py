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
    a = a.replace("{", " { ")
    a = a.replace("}", " } ")
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
    words = re.split("\n|\t|,| ", string) # Split the string into words
    tokens = []
    variables=[]
    procedures={}
    # Iterate over the string
    for i in range(len(words)):
        word=words[i] 
        # Conditions to check if parenthesis are present
        left_par=False
        right_par=False
        
        #Eliminating empty words
        if word==" " or word=="" or word=="\n" or word=="\t":
            continue
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

            if words[i-1].lower()=="defvar":
                tokens.append(word.lower())
                variables.append(word.lower())
            elif words[i-1].lower()=="defproc":
                tokens.append(word.lower())

                procedures[word.lower()]=[]
                j=1
                while words[i+j]!=")":
                    if words[i+j]!="," and words[i+j]!=" " and words[i+j]!="\n" and words[i+j]!="\t" and words[i+j]!="(" and words[i+j]!=";" and words[i+j]!="":
                        procedures[word.lower()].append(words[i+j])
                    j+=1
            elif word.lower() in variables:
                tokens.append(word.lower())
            elif word.lower() in procedures:
                tokens.append(word.lower())
            if len(procedures)>0:
                if word.lower() in procedures[list(procedures.keys())[-1]]:
                    tokens.append(word.lower())
           

        
        # Reinserting parenthesis into tokens
        if left_par:
            tokens.append("(")
        if right_par:
            tokens.append(")")
        

    # Return the list of tokens
    return tokens, variables, procedures


#Función que checkea todo el lenguaje de una vez. FALTA agregarle más cosas
def check_lenguage(tokens:list, variables:list, procedures:dict)->bool:
    confirmacion = True
    direcciones =["N","S","E","W","F","B","L","R","A"] 
    parametros_procedimientos = []
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
                    print("Fallo en la función.")
                    return confirmacion
                    
            else:
                confirmacion = False
                print("Fallo en la función 2")
                return confirmacion
        #Checkear declaracion de procedimientos 'P' ##¿¿ Los procedimientos siempre se declaran de primero? SI no se declaran de primero ahí si hay un problema
        elif tokens[i]== 'P':
            if tokens[i+1] in procedures:
                if tokens[i+2] == '(':
                    cantidad_parametros = len(procedures[tokens[i+1]])
                    if cantidad_parametros != 0:
                        for p in range(0,cantidad_parametros):
                            if tokens[i+3+p] in procedures[tokens[i+1]]:
                                parametros_procedimientos.append(tokens[i+3+p])
                                confirmacion = True
                            else:
                                confirmacion = False
                                print("Los parametros no coinciden")
                                return confirmacion
                    if tokens[i+2+cantidad_parametros+1] == ')':
                        confirmacion = True
                    elif tokens[i+2+cantidad_parametros+1] != ')':
                        confirmacion = False
                        print("En la declación de parametros no se cierra bien el parentesis0")
                        return confirmacion
                    #debido a que se está checkeando al principio que los corchetes si estén bien cerrados sabemos si esto está bien cerrado

                else:
                    confirmacion = False
                    print("En la declación de parametros no se abre bien el parentesis")
                    return confirmacion
        #Checkear procedimientos
        elif tokens[i] in procedures:
            len_parametros = len(procedures[tokens[i]])
            if tokens[i+1]=='(':
                if len_parametros!=0:
                    for z in range(0,len_parametros):
                        if tokens[i+2+z] =="#" or tokens[i+2+z] in procedures[tokens[i]] or tokens[i+2+z] in variables:
                            confirmacion=True
                        else:
                            confirmacion = False
                            print(tokens[i+2+z])
                            print("El parametro que se ingresó no es númerico, no funciona")
                            return confirmacion
                if tokens[i+1+len_parametros+1] == ')':
                    confirmacion = True
                else:
                    confirmacion = False
                    print("El procedimiento no tiene un parentesis de cierre bien puesto.")
                    return confirmacion
                
        #Checkear walk y leap
        elif tokens[i] in ["w","l"]:
            if tokens[i+1] == "(":
                if tokens[i+2] in variables or tokens[i+2]=="#":
                    if tokens[i+3]==")":
                        if tokens[i+4]== ";" or tokens[i+4]== "}" or tokens[i+4] ==")":
                            confirmacion=True
                        else:
                            confirmacion = False
                            print("no se cierra bien el comando")
                            return confirmacion
                    elif tokens[i+3] in direcciones:
                        if tokens[i+4] == ")":
                            if tokens[i+5]== ";" or tokens[i+5]== "}" or tokens[i+5] ==")":
                                confirmacion=True
                            else:
                                confirmacion = False
                                print("no se cierra bien el comando")
                                return confirmacion
                    else:
                        confirmacion = False
                        print(tokens[i+3])
                        print("No se cierra bien el parentesis1")
                        return confirmacion
                else:
                    confirmacion=False
                    print(i+1)
                    print(tokens[i+2])
                    print("error en el comando")
                    return confirmacion
            else:
                confirmacion = False
                print(i+1)
                print(tokens[i+1])
                print("error en el comando")
                return confirmacion
        #Checkear drop, get, grab
        elif tokens[i] in ["d","g","gr"]:
            if tokens[i+1] =="(":
                if tokens[i+2] == "#" or tokens[i+2] in variables or tokens[i+2] in parametros_procedimientos:
                    if tokens[i+3]== ")":
                        if tokens[i+4]== ";" or tokens[i+4]== "}" or tokens[i+4] ==")":
                            confirmacion=True
                        else:
                            confirmacion = False
                            print("no se cierra bien el comando")
                            return confirmacion
                    else:
                        confirmacion = False
                        print("No cumple con las indicaciones")
                        return confirmacion
                else:
                    confirmacion =False
                    print("No cumple con las indicaciones de parametros")
                    return confirmacion
            else:
                confirmacion = False
                print("No se abre bien para el drop, get, grab")
                return confirmacion
        #Checkear jump
        elif tokens[i] == "j":
            if tokens[i+1]=="(":
                if tokens[i+2] == "#" or tokens[i+2] in variables or parametros_procedimientos:
                    if tokens[i+3] == "#" or tokens[i+3] in variables or parametros_procedimientos:
                        if tokens[i+4] == ")":
                            confirmacion = True
                        else:
                            confirmacion = False
                            print("Jump no quedó bien cerrado")
                            return confirmacion
                    else:
                        confirmacion = False
                        print("Parametros de jump mal indicados")
                        return confirmacion
                else:
                    confirmacion = False
                    print("Parametros de jump mal indicados")
                    return confirmacion 
            else:
                confirmacion = False
                print("Parametros de jump mal indicados")
                return confirmacion
        #checkear turn, turnTO
        elif tokens[i] in ["T", "Tt"]:
            if tokens[i+1] == "(":
                if tokens[i+2] in direcciones:
                    if tokens[i+3] == ")":
                        confirmacion = True
                    else:
                        confirmacion = False
                        print(tokens[i+3])
                        print("No se cierra bien el parentesis2")
                        return confirmacion
                else:
                    confirmacion = False
                    print("Las indicaciones no están bien dadas")
                    return confirmacion
            else:
                confirmacion = False
                print("No se abre bien el parentesis")
                return confirmacion
        #Checkear nop
        elif tokens[i] == "nop":
            if tokens[i+1] == "(":
                if tokens[i+2] ==")":
                    confirmacion = True
                else:
                    confirmacion = False
                    print("Parentesis mal cerrado")
                    return confirmacion
            else:
                confirmacion = False
                print("Parentesis mal abierto")
                return confirmacion

        #Checkear while
        elif tokens[i]== "while":
            if tokens[i+1] == "can" or tokens[i+1]=="facing":
                if tokens[i+2]  =="(":
                    confirmacion = True
                else:
                    confirmacion = False
                    print("No se abre bien el parentesis")
                    return confirmacion
            elif tokens[i+1]=="not":
                if tokens[i+2] in ["can","facing"]:
                    if tokens[i+3] =="(":
                        confirmacion = True
                    elif tokens[i+2]=="not":
                        confimracion = True
                    else:
                        confirmacion = False
                        print("While mal escrito")
                        return confirmacion
        #checkear can
        elif tokens[i] == "can":
            if tokens[i+1] == "(":
                if tokens[i+2] in ["j","w","l","T","Tt","d","g", "gr","lg","nop"]:
                    confirmacion = True
                else:
                    confirmacion = False
                    print("Can mal escrito")
                    return confirmacion
            else:
                confirmacion = False
                print("Can mal escrito")
                return confirmacion
            
        #checkear if
        elif tokens[i] == "if":
            if tokens[i+1] in ["can", "facing", "not"]:
                confimracion=True
            else:
                confimracion = False
                print("if statement mal hecho")
                return confimracion
        #check else 
        elif tokens[i] == "else":
            if tokens[i+1] == "{":
                confirmacion = True
            else:
                confimracion = False
                print("Error en el else statement")
                return confirmacion
        #check repeat
        elif tokens[i] == "repeat":
            if tokens[i+1] in variables or tokens[i+1] == "#":
                if tokens[i+2] =="times":
                    if tokens[i+3] =="{":
                        confirmacion = True
                    else:
                        confimracion = False
                        print("Repeat mal hecho")
                        return confirmacion
                else:
                    confirmacion = False
                    print("Repeat mal hecho")
                    return confirmacion
            else:
                confimracion = False
                print("repeat mal hecho")
                return confimracion
        elif tokens[i] =="(":
            if tokens[i-1] in ["j","w","l","T","Tt","d","g", "gr","lg","nop", "can"] or tokens[i-1] in procedures or tokens[i-1] in parametros_procedimientos:
                confirmacion=True
            else:
                confirmacion = False
                print("No está definido bien bien bien")
                return confirmacion
        
    print("Funcionó bien")
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

if can ( walk ( 1 , west ) ) { walk ( 1 , west )} else { nop () } ;
goNorth () ;
goWest () ;

}
{
jump ( 4 ,5 ) ;
putCB ( 6 ,7 ) ;
goNorth () ;
goWest () ;
goNorth ()
}"""


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

if can ( walk ( 1 , west ) ) { walk ( 1 , west ) } else { nop () } ;
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
string_a_mirar=invalido2
print(parser(agregar_espacios(string_a_mirar)), check_lenguage(parser(agregar_espacios(string_a_mirar))[0],parser(agregar_espacios(string_a_mirar))[1],parser(agregar_espacios(string_a_mirar))[2]))