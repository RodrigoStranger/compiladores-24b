from sintactic import success, tree
from functions_semantic import *

tabla_de_simbolos = []
errores_semanticos = []

if success:
    recorrer_funciones(tree, tabla_de_simbolos, errores_semanticos)
    recorrer_main(tree, tabla_de_simbolos, errores_semanticos)
    imprimir_tabla_de_simbolos(tabla_de_simbolos)
    imprimir_resultado_errores(errores_semanticos)
else:
    print(" ")
    print("El análisis sintáctico ha fallado.")
