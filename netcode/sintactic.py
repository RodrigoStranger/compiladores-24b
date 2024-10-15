import os
import math

from functions_lexic import print_tokens
from functions_sintactic import arbolSintactico
from functions_sintactic import parser_sintactico_ll1
from lexic import listtokens
from functions_sintactic import generate_table_ll1
from graphviz import Digraph

directory2 = os.path.dirname(__file__)
sketchfile = 'table_ll1.csv'
pathfile2 = os.path.join(directory2, '..', 'table_ll1', sketchfile)

table_ll1 = generate_table_ll1(pathfile2)

success, arbol = parser_sintactico_ll1(listtokens, table_ll1)

if success:
    print("Análisis exitoso.")
    graph = arbolSintactico(arbol)
    output_folder = 'tree'
    if not os.path.exists(output_folder): os.makedirs(output_folder)
    output_pdf_path = os.path.join(output_folder, 'tree_sintactic_hola_mundo') 
    graph.render(output_pdf_path, format='png', view=True)
else:
    print("Error en el análisis sintáctico.")