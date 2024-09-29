from lexer import listtokens
from lexer import Token
from lexer import print_tokens
import pandas as pd
import os
import matplotlib.pyplot as plt

directory2 = os.path.dirname(__file__)
sketchfile = 'table_ll1_example.csv'
pathfile2 = os.path.join(directory2, '..', 'table_ll1', sketchfile)

output_folder = 'table_ll1'

if not os.path.exists(output_folder): os.makedirs(output_folder)

output_pdf_path = os.path.join(output_folder, 'table_ll1_example.png')

def generate_table_ll1(pathfile):
    df = pd.read_csv(pathfile, index_col = 0)
    df = df.fillna('null')
    return df

print("Tabla ll1:")

table_ll1 = generate_table_ll1(pathfile2)

print(table_ll1)

print(" ")

listtokens_example = []

# atributes: type , value, line, column
def generate_token_example(type, listtokens):
    token_obj = Token(type, type, 0, 0)
    listtokens.append(token_obj)

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

def generate_syntax_table(csv_path, output_png_path):
    table_print = generate_table_ll1(csv_path)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=table_print.values, 
                     colLabels=table_print.columns, 
                     rowLabels=table_print.index, 
                     loc='center', 
                     cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.2)
    for j in range(len(table_print.columns) + 1):
        for (i, j2) in table.get_celld().keys():
            if j2 == j: table[(i, j2)].set_width(0.2)
    plt.savefig(output_png_path, bbox_inches='tight', dpi=300)
    plt.close(fig)
    print(f"Imagen png generada exitosamente en: {output_png_path}")

print(" ")
print("Detalles del análisis sintáctico: ")
def ll1_parse(tokens, parsing_table):
    stack = ['$','E']
    index = 0
    while stack:
        print(f"Estado de la pila: {stack}, Tokens restantes: {[token.type for token in tokens[index:]]}")
        top = stack.pop()
        # si el símbolo en la cima es un terminal
        if top in [token.type for token in tokens]:  # compara con tipos de tokens
            if index < len(tokens) and tokens[index].type == top:
                print(f"Coincidencia encontrada: {top}")
                index += 1
            else:
                print(" ")
                print(f"Error: Se esperaba {top}, pero se encontró {tokens[index].type if index < len(tokens) else 'fin de entrada'}")
                return False
        # si el símbolo en la cima es un no terminal
        elif top in parsing_table.index:
            if index < len(tokens):
                current_token = tokens[index].type
                production = parsing_table.at[top, current_token]
                if production != 'null':
                    # descomponer la producción y añadir al stack
                    if production != 'e':
                        print(f"Producción encontrada para {top}: {production}")
                        stack.extend(reversed(production.split()))  # añadir en orden inverso
                    else:
                        print(f"Producción vacía encontrada para {top}")
                else:
                    print(" ")
                    print(f"Error: No hay producción válida para {top} con el token {current_token}")
                    return False  # no hay producción válida
            else:
                print(" ")
                print("Error: Se acabaron los tokens, pero aún hay no terminales en el stack")
                return False  # se acabaron los tokens, pero aún hay no terminales en el stack
        else:
            print(" ")
            print(f"Error: símbolo no reconocido {top}")
            return False  # símbolo no reconocido
    # verifica si se ha consumido toda la entrada
    success = index == len(tokens)
    if success:
        print(" ")
        print("Análisis exitoso.")
    else:
        print(" ")
        print("Falló el análisis.")
    return success

result = ll1_parse(listtokens_example, table_ll1)
print("Resultado del análisis ll(1):", result)

generate_syntax_table(pathfile2, output_pdf_path)