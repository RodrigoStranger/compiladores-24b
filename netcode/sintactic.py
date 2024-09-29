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
generate_token_example("+", listtokens_example)
generate_token_example("int", listtokens_example)
generate_token_example("$", listtokens_example)

#print_tokens(listtokens_example)

print(" ")
print("Detalles del análisis sintactico: ")
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
                    print(f"Error: No hay producción válida para {top} con el token {current_token}")
                    return False  # no hay producción válida
            else:
                print("Error: Se acabaron los tokens, pero aún hay no terminales en el stack")
                return False  # se acabaron los tokens, pero aún hay no terminales en el stack
        else:
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

result = ll1_parse(listtokens_example, df)
print(" ")
print("Resultado del análisis ll(1):", result)