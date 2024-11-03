from sintactic import parse_tree_root, success
from functions_semantic import *

if success:
    tabla_simbolos = construir_tabla_de_simbolos(parse_tree_root)
    for simbolo in tabla_simbolos:
        print(f"Nombre: {simbolo.nom_sym}, Tipo: {simbolo.tipo_data}, Contexto: {simbolo.function}, Valor: {simbolo.valor}")
else: 
    print(" ")
    print("El análisis sintáctico ha fallado.")
    