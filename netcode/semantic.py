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
# lo que falta es agregar recorrer_cuerpo_main, recorrer_cuerpo_function, 
# ya esta el tema de verificacion de parametros de funciones, falta el de llamadas, y que las dos tengan el mismo conteo
# las veriicaciones de retorno deben mudarse a la verificacion de cuerpo tanton de main como de las propias funciones.
if success:
    recorrer_funciones(tree, tabla_de_simbolos, errores_semanticos)
    recorrer_main(tree, tabla_de_simbolos, errores_semanticos)
    
    
    imprimir_tabla_de_simbolos(tabla_de_simbolos)
    imprimir_resultado_errores(errores_semanticos)
else:
    print(" ")
    print("El análisis sintáctico ha fallado.")