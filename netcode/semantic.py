from sintactic import success, tree
from functions_semantic_scope import *
from functions_semantic_type import *

tabla_de_simbolos = []
errores_semanticos = []

if success:
    #ambitos:
    recorrer_funciones(tree, tabla_de_simbolos, errores_semanticos)
    recorrer_main(tree, tabla_de_simbolos, errores_semanticos)
    #tipos:

    imprimir_tabla_de_simbolos(tabla_de_simbolos)
    imprimir_resultado_errores(errores_semanticos)
else:
    print(" ")
    print("El análisis sintáctico ha fallado.")