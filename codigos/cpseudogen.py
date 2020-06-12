import sys
import re

import os.path
from os import path

reglas = [
    ["return 0;\n}","\nFIN;"],
    ["return 0;}","\nFIN;"],
    ["return 1;\n}","\nFIN;"],
    ["return 1;}","\nFIN;"],
    ["return 0;","FIN;"],
    ["return 1;","FIN;"],
    ["printf","Imp"],
    ["scanf","Leer"],
    ["for ","Para "],
    ["if (","Si ("],
    ["else","else "],
    ["else ","Sino "],
    ["while ","Mientras "],
    ["do {","Hacer {"],
    ["int argc,char **argv",""],
    ["int main(void)","int main()"],
    ["int main()\n{","INICIO;"],
    ["int main(){","INICIO;"],
    ["Sino  Si ","SinoSi "],
    ['\\' + 'n',""], #quitar \n de printfs y demas
    ["\n    ","\n"]] #quitar 1 tabulacion



stdioSpecifiers = ['c', 'd', 'i', 'e', 'E', 'f', 'g', 'G', 'o', 's', 'u', 'x', 'X', 'p', 'n', '%']
stdioVarEnd = [' ', ',', ')']

class stdioVarPlaceholder():
    def __init__(self, found, text, specifier, startIndex, endIndex):
        self.found = found
        self.text = text
        self.specifier = specifier
        self.startIndex = startIndex
        self.endIndex = endIndex
def getStdioVarPlaceholder(st, startIndex):
    endIndex = 0
    try:
        firstIndex = st.index("%", startIndex)
    except ValueError:
        return(stdioVarPlaceholder(0, "", '', 0, 0))
        
    lowestendIndex = len(st)
    foundspecifier = ''

    for specifier in stdioSpecifiers:
        try:
            endIndex = st.index(specifier, firstIndex + 1)
            if (endIndex <= lowestendIndex):
                lowestendIndex = endIndex
                foundspecifier = specifier
        except ValueError:
            endIndex = lowestendIndex
    
    endIndex = lowestendIndex
    
    text = str(st[firstIndex:endIndex + 1])
    return(stdioVarPlaceholder(1, text, foundspecifier, firstIndex, endIndex))
def getStdioVarReplace(st, startIndex):
    endIndex = 0
    try:
        firstIndex = st.index(" ", startIndex)
    except ValueError:
        return(stdioVarPlaceholder(0, "", '', 0, 0))
        
    lowestendIndex = len(st)
    foundspecifier = ''

    for specifier in stdioVarEnd:
        try:
            endIndex = st.index(specifier, firstIndex + 1)
            if (endIndex <= lowestendIndex):
                lowestendIndex = endIndex
                foundspecifier = specifier
        except ValueError:
            endIndex = lowestendIndex
    endIndex = lowestendIndex
    
    text = str(st[firstIndex + 1:endIndex])
    return(stdioVarPlaceholder(1, text, foundspecifier, firstIndex, endIndex))
def getVarList(st, startIndex):
    varList = []
    try:
        firstVar = getStdioVarPlaceholder(st, startIndex)
        if (firstVar.found == 0):
            return(varList)
        else:
            lastIndex = firstVar.endIndex + 1
            varList.append(firstVar)
    
            while getStdioVarPlaceholder(st, lastIndex).found == 1:
                varList.append(getStdioVarPlaceholder(st, lastIndex))
                lastIndex = getStdioVarPlaceholder(st, lastIndex).endIndex + 1
    except ValueError:
        varList = []
    return(varList)

def getReplaceVarList(st, startIndex):
    varList = []
    try:
        firstVar = getStdioVarReplace(st, startIndex)
        if (firstVar.found == 0):
            return(varList)
        else:
            lastIndex = firstVar.endIndex + 1
            varList.append(firstVar)

            while getStdioVarReplace(st, lastIndex).found == 1:
                varList.append(getStdioVarReplace(st, lastIndex))
                lastIndex = getStdioVarReplace(st, lastIndex).endIndex + 1
    except ValueError:
        varList = []
    return(varList)
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
def sfind_between( s, first, last ):
    try:
        start = s.index( first ) 
        end = s.index( last, start ) + len( last )
        return s[start:end]
    except ValueError:
        return ""
def del_closedcomment(src):
    comentario=sfind_between(src,"/*","*/")
    return(src.replace(comentario, ""))
def delete_includes(src): #Elimina includes.
    print("\nEliminando includes...")
    src_out = ""
    for index, line in enumerate(src.splitlines(), start=1):
        if (not line.startswith('#include')):
                src_out += line + '\n'
        else:
            print(" - [Linea: " + str(index) + "] " + line)
    return(src_out)
def delete_defines(src): #Elimina defines.
    print("\nEliminando defines...")
    src_out = ""
    for index, line in enumerate(src.splitlines(), start=1):
        if (not line.startswith('#define')):
                src_out += line + '\n'
        else:
            print(" - [Linea: " + str(index) + "] " + line)
    return(src_out)
def delete_commentlines(src): #elimina comentarios.
    print("\nEliminando comentarios de linea...")
    src_out = ""
    for i, line in enumerate(src.splitlines(), start=1):
        try:
            start = line.index( "//" )
            comentario = line[start:len(line)]
            print(comentario)
            line = line.replace(comentario, "")
            src_out += line + "\n"
        except ValueError:
            src_out += line + "\n"
            
            
    return(src_out)
def delete_commentclosed(src): #elimina comentarios cerrados.
    print("\nEliminando comentarios cerrados...")
    src_out = src

    while src_out.count("/*") > 0:
        comentario=sfind_between(src_out,"/*","*/")
        comentariopt=comentario.replace("\n","")
        src_out = src_out.replace(comentario, "")
        print(" - " + comentariopt)

    return(src_out)
def delete_blanks(src): #elimina lineas en blanco
    print("\nEliminando Lineas en blanco...")
    src_out = ""
    for index, line in enumerate(src.splitlines(), start=1):
        if (not line.isspace()):
            if ((line and line.strip())):
                src_out += line + '\n'
            else:
                print(" - [Linea: " + str(index) + "]")
        else:
            print(" - [Linea: " + str(index) + "]")
    return(src_out)
def processtdio(src):
    print("\nCorrigiendo printf's...")
    src_out = ""
    for i, line in enumerate(src.splitlines(), start=1):
        try:
            printfstart = line.index( "printf" )
            printf_parentesis_start = line.index("(", printfstart)
            varList = getVarList(line, printf_parentesis_start)
            if (len(varList) > 0):
                printf_string_end = line.index("\",", printf_parentesis_start) + 1
                printf_end = line.index(");", printf_string_end)
                replaceVarList = getReplaceVarList(line, printf_string_end)
                line = line.replace(line[printf_string_end:printf_end], "")
                #reemplazar variables...
                replaceTasks = ""
                for index, var_s in enumerate(varList, start=0):
                    destvar = var_s.text
                    fromvar = "$" + str(replaceVarList[index].text)
                    line = line.replace(destvar, fromvar)
                    replaceTasks += destvar + " -> " + fromvar + "  "
                print(" - [Linea: " + str(i) + "] " + replaceTasks)
        except ValueError:
            pass
        src_out += line + "\n"

    print("\nCorrigiendo scanf's...")
    src_out_2 = ""
    for i, line in enumerate(src_out.splitlines(), start=1):
        try:
            scanfstart = line.index( "scanf" )
            scanf_parentesis_start = line.index("(", scanfstart)
            scanf_string_start = line.index("(\"", scanf_parentesis_start) + 1
            scanf_string_end = line.index("\",", scanf_string_start) + 3
            line = line.replace(line[scanf_string_start:scanf_string_end], "")
            line = line.replace("&", "")
            print(" - [Linea: " + str(i) + "] " + line[scanfstart:len(line)])
        except ValueError:
            pass
        src_out_2 += line + "\n"
    return(src_out_2)

#Inicializar el programa
if len(sys.argv) != 2:
    print("Error, especifique archivo de entrada")
    print("ejemplo: <python3 c-to-pseudo.py test.c>")
    exit()

filename = sys.argv[1]
outputfilename = filename.replace(".c", "-pseudo.txt")



if not path.exists(filename):
    print("No se encontro el archivo: <" + filename + ">")
    exit()

#Todo OK!
print("Abriendo el archivo: <" + filename + ">")
sourcefile = open(filename, "r").read()



#eliminar includes, defines, lineas vacias, comentarios, etc. primera pasada
source = delete_includes(sourcefile)
source = delete_defines(source)
source = delete_commentlines(source)
source = delete_commentclosed(source)
source = delete_blanks(source)

#procesar printf y scanf (stdio)
source = processtdio(source)
print(source)

#ejecutar reglas de reemplazo simples.
for regla in reglas:
    source = source.replace(regla[0], regla[1])

#eliminar includes, defines, lineas vacias, comentarios, etc. segunda pasada
source = delete_blanks(source)






print("\nEscribiendo el archivo: <" + outputfilename + ">.")
output = open(outputfilename, "w+")
output.write(source)
print("Listo.")