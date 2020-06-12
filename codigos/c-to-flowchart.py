import sys
import re
from enum import Enum

reglas = [
    ["return 0;\n}","\nFIN"],
    ["printf","Imp"],
    ["scanf","Leer"],
    ["for","Para"],
    ["if","Si"],
    ["else","Sino"],
    ["while","Mientras"],
    ["do","Hacer"],
    ["int argc,char **argv",""],
    ["int main(void)","int main()"],
    ["int main()\n{","INICIO"],
    ["int main(){","INICIO"],
    ['\\' + 'n',""], #quitar \n de printfs y demas
    ["\n    ","\n"],
    ["%", "-"]] #quitar 1 tabulacion

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def eliminar1(src):
    src_out = ""
    for line in src.splitlines():
        if (not (line.startswith('#') or line.startswith("//")) and not line.isspace()):
            if ((line and line.strip())):
                src_out += line + '\n'
    return(src_out)


if len(sys.argv) != 3:
    print("Error, especifique archivo de entrada y salida:")
    print("ejemplo: <python3 c-to-pseudo.py test.c pseudo.txt>")
    exit()
filename = sys.argv[1]
outputfilename = sys.argv[2]

print("Convirtiendo el archivo: <" + filename + "> a pseudocodigo.")
print("Archivo de salida: <" + outputfilename + ">.")
sourcefile = open(filename, "r").read()

#eliminar includes, defines, lineas vacias, comentarios, etc. primera pasada
source = eliminar1(sourcefile)

#eliminar comentarios de tipo /*  */
firstDelPos=source.find("/*") # get the position of [
secondDelPos=source.find("*/") # get the position of ]
source = source.replace(source[firstDelPos:secondDelPos+2], "") # remove the string between two delimiters


#ejecutar reglas de reemplazo simples.
for regla in reglas:
    source = source.replace(regla[0], regla[1])


#eliminar includes, defines, lineas vacias, comentarios, etc. segunda pasada
pseudo = eliminar1(source)

sourceLineList = pseudo.splitlines()

tikznodedistanceval = 2
tikznodedistanceunit = "cm"
tikznodedistance = str(tikznodedistanceval) + tikznodedistanceunit
tikzfileheader = "\\begin{center}\n    \\begin{tikzpicture}[node distance=" + tikznodedistance + "]"
tikzfilefooter = "\n    \\end{tikzpicture}\n\\end{center}"

output = tikzfileheader


#Generar lista de elementos
class ElementType(Enum):
    START = "START"
    STOP = "STOP"
    PROCESS = "PROCESS"
    OUTPUT = "OUTPUT"
    INPUT = "INPUT"
    IF = "IF"
    ELSEIF = "ELSEIF"
    WHILE = "WHILE"
    FOR = "FOR"

class NextElementPos(Enum):
    BELOW = "below"
    TOP = "top"
    RIGHT = "right"
    LEFT = "left"

class Element():
    def __init__(self, elType, nextPos, argument, lineNumber): #lineNumber haria de ID
        self.elType = elType
        self.nextPos = nextPos
        self.lineNumber = lineNumber
        self.argument = argument
        self.nodeName = str(elType.value).lower() + str(lineNumber)

ElementList = []

def printElement(elemento):
    print("NodeName: " + elemento.nodeName + " L-" + str(Element.lineNumber) + ": " + Element.elType.value + " arg: " + Element.argument)
    return

#Formular string a partir de un elemento.
def tikzFromElement(ElementId):
    returnTxt = ""
    elemento = ElementList[ElementId]
    placeString = ""
    if (ElementId > 0): #no es el primer elemento.
        ultimoElemento = ElementList[ElementId - 1]
        placeString = ", " + ultimoElemento.nextPos.value + " of=" + ultimoElemento.nodeName
        if (ultimoElemento.elType == ElementType.FOR):
            placeString += ", yshift=-0.5cm"
        if (ultimoElemento.nextPos == NextElementPos.RIGHT):
            placeString += ", xshift=2cm"
        if (ultimoElemento.nextPos == NextElementPos.LEFT):
            placeString += ", xshift=-2cm"


    if (elemento.elType == ElementType.START):
        returnTxt = "\n    \\node (" + elemento.nodeName + ") [startstop" + placeString + "] {Inicio};"
    if (elemento.elType == ElementType.STOP):
        returnTxt = "\n    \\node (" + elemento.nodeName + ") [startstop" + placeString + "] {Fin};"
    if (elemento.elType == ElementType.OUTPUT):
        returnTxt = "\n    \\node (" + elemento.nodeName + ") [io" + placeString + "] {Imp: " + elemento.argument + "};"
    if (elemento.elType == ElementType.INPUT):
        returnTxt = "\n    \\node (" + elemento.nodeName + ") [io" + placeString + "] {Leer: " + elemento.argument + "};"
    if (elemento.elType == ElementType.FOR):
        returnTxt = "\n    \\node (" + elemento.nodeName + ") [for" + placeString + ", yshift=-0.5cm] {" + elemento.argument + "};"
    

    return(returnTxt)
    


#buscar elementos en el pseudocodigo y almacenarlos en la lista.
arg = ""
for index, line in enumerate(sourceLineList, start=1):
    if ("INICIO" in line):
        ElementList.append(Element(ElementType.START, NextElementPos.BELOW, "", index))
    if ("FIN" in line):
        ElementList.append(Element(ElementType.STOP, NextElementPos.BELOW, "", index))
    if ("Imp(""" in line):
        arg = find_between(line, "Imp(""", ");").replace("\"", "")
        ElementList.append(Element(ElementType.OUTPUT, NextElementPos.BELOW, arg, index))
    if ("Para (""" in line):
        arg = find_between(line, "Para (""", ")")
        ElementList.append(Element(ElementType.FOR, NextElementPos.BELOW, arg, index))


#Imprimir lista de elementos.
print("\n\n\nImprimiendo la lista de elementos reconocidos:\n")
for index, Element in enumerate(ElementList, start=1):
    printElement(Element)
print("\nFin de la lista\n")


def genTikzArrow(elemento_origen, elemento_destino):
    returnStr = "\n    FLECHA"
    returnStr = "\n    \\draw [arrow] (" + elemento_origen.nodeName + ") -- (" + elemento_destino.nodeName + ");"
    return(returnStr)



#Generar elementos.
output += "\n\n    %Nodos"
for index, Element in enumerate(ElementList, start=0):
    output += tikzFromElement(index)

output += "\n\n    %Flechas"
#Generar Flechas.
for index, Element in enumerate(ElementList, start=0):
    if (index < len(ElementList) - 1):
        output += genTikzArrow(Element, ElementList[index + 1])

output += tikzfilefooter
#print("Agregando linea: <" + tikzfilefooter + ">")

print("\nImprimiendo archivo generado: \n")
print(output)
print("\nFin del archivo\n")
#output = open(outputfilename, "w+")
#output.write(source)