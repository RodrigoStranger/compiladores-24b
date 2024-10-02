import os
from lexic import listtokens

from functions import generate_table_ll1
from functions import generate_token_example
from functions import ll1_parse
from functions import ll1_parse_use_objects

directory2 = os.path.dirname(__file__)
sketchfile = 'table_ll1.csv'
pathfile2 = os.path.join(directory2, '..', 'table_ll1', sketchfile)

output_folder = 'tree'
if not os.path.exists(output_folder): os.makedirs(output_folder)
output_pdf_path = os.path.join(output_folder, 'tree_sintactic.png')


table_ll1 = generate_table_ll1(pathfile2)
generate_token_example("$", listtokens)

print("Entrada:",' '.join(token.type for token in listtokens))
print(" ")

print("Detalles del análisis sintáctico: ")
result= ll1_parse_use_objects(listtokens, table_ll1)

print("Resultado del análisis ll(1):", result)