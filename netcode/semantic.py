from sintactic import success, tree
from functions_semantic import *

if success:
    tabla_de_simbolos = []
    print("Creacion de Símbolos:")
    crear_simbolo_func(tree, tabla_de_simbolos)
    procesar_main(tree, tabla_de_simbolos)
    print("\nTabla de Símbolos")
    for simbolo in tabla_de_simbolos:
        print(simbolo)
else:
    print(" ")
    print("El análisis sintáctico ha fallado.")