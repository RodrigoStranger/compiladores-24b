from sintactic import success, tree
from functions_semantic import *

if success:
    pila_simbolos = []
    recorrer_preorden(tree, pila_simbolos)
    # Imprimir la tabla de símbolos generada
    print("Tabla de Símbolos:")
    for simbolo in pila_simbolos:
        print(simbolo)
else:
    print(" ")
    print("El análisis sintáctico ha fallado.")