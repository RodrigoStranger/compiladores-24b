import pandas as pd
import matplotlib.pyplot as plt
from graphviz import Digraph

from functions_lexic import Token

#funcion que genera una tabla ll1 
def generate_table_ll1(pathfile):
    df = pd.read_csv(pathfile, index_col = 0)
    df = df.fillna('null')
    return df

#funcion que genera tokens
#atributes: type , value, line, column
def generate_token_example(type, listtokens):
    token_obj = Token(type, type, 0, 0)
    listtokens.append(token_obj)

#funcion que genera un png de una tabla ll1
def generate_syntax_table_png(csv_path, output_png_path):
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
            if j2 == j: table[(i, j2)].set_width(0.3)
    plt.savefig(output_png_path, bbox_inches='tight', dpi=300)
    plt.close(fig)
    print(f"Imagen png generada exitosamente en: {output_png_path}")

#funcion que verifica con el algoritmo ll1
def ll1_parse(tokens, parsing_table):
    stack = ['$','NETCODE']
    index = 0
    while stack:
        print(f"Estado de la pila: {stack}, Tokens restantes: {[token.type for token in tokens[index:]]}")
        top = stack.pop()
        # si el símbolo en la cima es un terminal
        if top in [token.type for token in tokens]:
            if index < len(tokens) and tokens[index].type == top:
                print(f"Coincidencia encontrada: {top}")
                index += 1
            else:
                print("\nError: Se esperaba '{}' pero se encontró '{}'".format(
                    top, tokens[index].type if index < len(tokens) else 'fin de entrada'))
                print("Lista de tokens restantes: ", [token.type for token in tokens[index:]])
                return False
        # si el símbolo en la cima es un no terminal
        elif top in parsing_table.index:
            if index < len(tokens):
                current_token = tokens[index].type
                try:
                    production = parsing_table.at[top, current_token]
                    if production != 'null':
                        # descomponer la producción y añadir al stack
                        if production != 'e':  # 'e' representa la producción vacía
                            print(f"Producción encontrada para {top}: {production}")
                            stack.extend(reversed(production.split()))  # añadir en orden inverso
                        else:
                            print(f"Producción vacía encontrada para {top}")
                    else:
                        print("\nError: No hay producción válida para el no terminal '{}' con el token '{}'".format(
                            top, current_token))
                        print("Lista de tokens restantes: ", [token.type for token in tokens[index:]])
                        return False
                except KeyError as e:
                    print(f"\nError: No se encontró una producción en la tabla LL(1) para el no terminal '{top}' con el token '{current_token}'.")
                    print("Error específico:", str(e))
                    return False
            else:
                print("\nError: Se acabaron los tokens, pero aún hay no terminales en la pila: ", stack)
                return False
        # símbolo no reconocido (ni terminal ni no terminal)
        else:
            print("\nError: símbolo no reconocido en la pila '{}'".format(top))
            print("Lista de tokens restantes: ", [token.type for token in tokens[index:]])
            return False
    # verifica si se ha consumido toda la entrada
    success = index == len(tokens)
    if success:
        print("\nAnálisis exitoso.")
    else:
        print("\nFalló el análisis. Se esperaban más tokens pero la entrada se terminó.")
        print("Lista de tokens restantes: ", [token.type for token in tokens[index:]])
    return success