import os
from lexic import listtokens
from functions_sintactic import *

directory2 = os.path.dirname(__file__)
sketchfile = 'table_ll1_netcode.csv'
pathfile2 = os.path.join(directory2, '..', 'table_ll1', sketchfile)

table_ll1 = generate_table_ll1(pathfile2)
simboloinicial = "NETCODE"
success, tree = parser_sintactico_ll1(listtokens, table_ll1, simboloinicial)

#recorrer_arbol_por_id(tree)

'''
if success:
    output_folder = 'tree'
    if not os.path.exists(output_folder): os.makedirs(output_folder)
    graph = arbolSintactico(tree, True, "tipo") # arbol, si se quiere con contorno en las hojas o no, que atributo del nodo se desea imprimir
    output_pdf_path = os.path.join(output_folder, 'tree_hola_mundo4') 
    graph.render(output_pdf_path, format='png', view = True)
else:
    print(" ")
    print("El análisis sintáctico ha fallado.")
'''