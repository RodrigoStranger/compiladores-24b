from sintactic import success, tree
from functions_semantic import *

tabla_de_simbolos = []
errores_semanticos = []

'''
funcionactual = "F2"
tabla_de_simbolos = []
# Llamada a la función para contar los parámetros de la función especificada
num_parametros = buscar_y_verificar_parametros(funcionactual, tree, tabla_de_simbolos)
for simbolo in tabla_de_simbolos:
    print(simbolo)
'''

if success:
    recorrer_funciones(tree, tabla_de_simbolos, errores_semanticos)
    #procesar_main(tree, tabla_de_simbolos)
    
    
    imprimir_tabla_de_simbolos(tabla_de_simbolos)
    imprimir_resultado_errores(errores_semanticos)
else:
    print(" ")
    print("El análisis sintáctico ha fallado.")