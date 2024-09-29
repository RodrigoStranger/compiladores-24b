from lexer import listtokens
from lexer import Token
from lexer import print_tokens
import pandas as pd
import os

directory2 = os.path.dirname(__file__)
sketchfile = 'table_ll1_example.csv'
pathfile2 = os.path.join(directory2, '..', 'table_ll1', sketchfile)

df = pd.read_csv(pathfile2, index_col = 0)
df = df.fillna('null')
print("Tabla ll1:")
print(df)

listtokens_example = []
def generate_token_example(type, listtokens):
    token_obj = Token(type, type, 0, 0)
    listtokens.append(token_obj)

# aqui podemos introducir ejemplos:
generate_token_example("(", listtokens_example)
generate_token_example("int", listtokens_example)
generate_token_example(")", listtokens_example)
#generate_token_example("+", listtokens_example)
#generate_token_example("int", listtokens_example)  # Añadido para una prueba más completa
generate_token_example("$", listtokens_example)

#print_tokens(listtokens_example)

print(" ")

def ll1_parse(tokens, parsing_table):
    stack = ['$','E']
    index = 0
    while stack:
        top = stack.pop()
        # si el símbolo en la cima es un terminal
        if top in [token.type for token in tokens]:
            if index < len(tokens) and tokens[index].type == top:
                index += 1
            else:
                return False
        # si el símbolo en la cima es un no terminal
        elif top in parsing_table.index:
            if index < len(tokens):
                current_token = tokens[index].type
                production = parsing_table.at[top, current_token]
                if production != 'null':
                    if production != 'e':
                        stack.extend(reversed(production.split()))  # agregar en un orden inverso
                else:
                    return False  # no existe producción válida
            else:
                return False  # se acabaron los tokens, pero aún hay no terminales en el stack

        else:
            return False  # símbolo no reconocido
    # Verifica si se ha consumido toda la entrada
    return index == len(tokens)

# Ejecutar el análisis
result = ll1_parse(listtokens_example, df)
print("Resultado del análisis ll(1):", result)