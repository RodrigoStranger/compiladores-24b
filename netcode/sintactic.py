import os
from lexer import listtokens
from lexer import print_tokens

from functions import generate_table_ll1
from functions import generate_token_example
from functions import generate_syntax_table
from functions import ll1_parse

directory2 = os.path.dirname(__file__)
sketchfile = 'table_ll1_example.csv'
pathfile2 = os.path.join(directory2, '..', 'table_ll1', sketchfile)

output_folder = 'table_ll1'
if not os.path.exists(output_folder): os.makedirs(output_folder)
output_pdf_path = os.path.join(output_folder, 'table_ll1_example.png')

print("Tabla ll1:")

table_ll1 = generate_table_ll1(pathfile2)

print(table_ll1)

print(" ")

listtokens_example = []

# aqui podemos introducir ejemplos:
generate_token_example("(", listtokens_example)
generate_token_example("int", listtokens_example)
generate_token_example(")", listtokens_example)
generate_token_example("+", listtokens_example)
generate_token_example("int", listtokens_example)


'''
generate_token_example("if", listtokens_example)
generate_token_example("true", listtokens_example)
generate_token_example("then", listtokens_example)
generate_token_example("{", listtokens_example)
generate_token_example("true", listtokens_example)
generate_token_example("}", listtokens_example)
generate_token_example("else", listtokens_example)
generate_token_example("{", listtokens_example)
generate_token_example("if", listtokens_example)
generate_token_example("false", listtokens_example)
generate_token_example("then", listtokens_example)
generate_token_example("{", listtokens_example)
generate_token_example("false", listtokens_example)
generate_token_example("}", listtokens_example)
generate_token_example("}", listtokens_example)
'''

'''
generate_token_example("if", listtokens_example)
generate_token_example("true", listtokens_example)
generate_token_example("then", listtokens_example)
generate_token_example("{", listtokens_example)
generate_token_example("if", listtokens_example)
generate_token_example("false", listtokens_example)
generate_token_example("then", listtokens_example)
generate_token_example("{", listtokens_example)
generate_token_example("}", listtokens_example)
generate_token_example("else", listtokens_example)
generate_token_example("{", listtokens_example)
generate_token_example("}", listtokens_example)
generate_token_example("}", listtokens_example)
'''

# nunca comentar
generate_token_example("$", listtokens_example)

#print_tokens(listtokens_example)
print("Entrada:",' '.join(token.type for token in listtokens_example))

print(" ")

print("Detalles del análisis sintáctico: ")

result = ll1_parse(listtokens_example, table_ll1)

print("Resultado del análisis ll(1):", result)

generate_syntax_table(pathfile2, output_pdf_path)