from sintactic import success, tree
from functions_semantic import *


funcionactual = "F2"
tabla_de_simbolos = []
# Llamada a la función para contar los parámetros de la función especificada
num_parametros = buscar_y_verificar_parametros(funcionactual, tree, tabla_de_simbolos)
for simbolo in tabla_de_simbolos:
    print(simbolo)
'''
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
    '''