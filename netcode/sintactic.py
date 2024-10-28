import os
from lexic import listtokens
from functions_sintactic import generate_table_ll1
from functions_sintactic import arbolSintactico
from functions_sintactic import arbolSintacticoContorno
from functions_sintactic import parser_sintactico_ll1

directory2 = os.path.dirname(__file__)
sketchfile = 'table_ll1_netcode.csv'
pathfile2 = os.path.join(directory2, '..', 'table_ll1', sketchfile)

table_ll1 = generate_table_ll1(pathfile2)

simboloinicial = "NETCODE"

success, parse_tree_root = parser_sintactico_ll1(listtokens, table_ll1, simboloinicial)

'''
if success:
    output_folder = 'tree'
    if not os.path.exists(output_folder): os.makedirs(output_folder)
    graph = arbolSintacticoContorno(parse_tree_root)
    #graph = arbolSintactico(parse_tree_root)
    output_pdf_path = os.path.join(output_folder, 'tree_sintactic_func_semantic_var') 
    graph.render(output_pdf_path, format='png', view=True)
else:
    print(" ")
    print("El análisis sintáctico ha fallado.")
'''