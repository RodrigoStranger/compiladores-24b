from lexic import listtokens
import os
from functions_sintactic import generate_table_ll1
from functions_sintactic import arbolSintactico
from functions_sintactic import parser_sintactico_ll1

directory2 = os.path.dirname(__file__)
sketchfile = 'table_ll1_parent.csv'
pathfile2 = os.path.join(directory2, '..', 'table_ll1', sketchfile)

table_ll1 = generate_table_ll1(pathfile2)

success, parse_tree_root = parser_sintactico_ll1(listtokens, table_ll1)

if success:
    output_folder = 'tree'
    if not os.path.exists(output_folder): os.makedirs(output_folder)
    graph = arbolSintactico(parse_tree_root)
    output_pdf_path = os.path.join(output_folder, 'tree_sintactic') 
    graph.render(output_pdf_path, format='png', view=True)
else:
    print(" ")
    print("El análisis sintáctico ha fallado.")