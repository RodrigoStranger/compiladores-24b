from functions_semanctic import *
from functions_semantic_scope import *

def recorrer_main_type(node, tabla_de_simbolos, errores):
    if node.tipo == "MAIN":
        evaluar_asignaciones_type(node, tabla_de_simbolos, errores, "main")
    for hijo in node.hijos: recorrer_main(hijo, tabla_de_simbolos, errores)

def evaluar_asignaciones_type(node, tabla_de_simbolos, errores, ambitoactual):
    print()