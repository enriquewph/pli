import sys
import re

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
    ["\n    ","\n"]] #quitar 1 tabulacion

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
source = eliminar1(source)

output = open(outputfilename, "w+")
output.write(source)