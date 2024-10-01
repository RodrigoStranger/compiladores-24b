import os
from lexer import listtokens
from lexer import print_tokens

from functions import generate_table_ll1
from functions import generate_token_example
from functions import generate_syntax_table
from functions import ll1_parse

directory2 = os.path.dirname(__file__)
sketchfile = 'table_ll1.csv'
pathfile2 = os.path.join(directory2, '..', 'table_ll1', sketchfile)

output_folder = 'table_ll1'
if not os.path.exists(output_folder): os.makedirs(output_folder)
output_pdf_path = os.path.join(output_folder, 'table_ll1.png')

#print("Tabla ll1:")

table_ll1 = generate_table_ll1(pathfile2)

#print(table_ll1)
#print(" ")

# nunca comentar
generate_token_example("$", listtokens)

#print_tokens(listtokens_example)

print("Entrada:",' '.join(token.type for token in listtokens))
print(" ")

print("Detalles del análisis sintáctico: ")
result = ll1_parse(listtokens, table_ll1)

print("Resultado del análisis ll(1):", result)