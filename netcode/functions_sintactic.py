import pandas as pd
import matplotlib.pyplot as plt
from graphviz import Digraph
import math
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

class Simbolo:
    def __init__(self, tipo_data, nom_sym, function, valor=None):
        self.tipo_data = tipo_data
        self.nom_sym = nom_sym
        self.function = function
        self.valor = valor

class Arbol:
    def __init__(self, simbolo_lexer, lexema, line, column, es_terminal, id, tipo_data=None, valor=None):
        self.id = id
        self.lexema = lexema
        self.simbolo_lexer = simbolo_lexer
        self.es_terminal = es_terminal
        self.line = line
        self.column = column
        self.children = []
        self.padre = None
        self.simbolos = []
        self.tipo_data = tipo_data
        self.valor = valor

    def agregar_simbolo(self, tipo_data, nom_sym, function, valor=None):
        simbolo_lexer = Simbolo(tipo_data, nom_sym, function, valor=valor)
        self.simbolos.append(simbolo_lexer)
        self.tipo_data = tipo_data
        self.valor = valor

class Pila:
    def __init__(self, simbolo, es_terminal):
        global count
        self.id = count
        self.simboloLex = simbolo
        self.es_terminal = es_terminal
        count += 1

def buscar(node, id):
    if node.id == id:
        return node
    for c in node.children:
        found_node = buscar(c, id)
        if found_node is not None:
            return found_node
    return None

def arbolSintactico(raiz):
    graph = Digraph()
    def generar_nodos(node):
        label = f"{node.simbolo_lexer}"
        if node.line is not None:
            label += f"\nline: {node.line}"
        if node.column is not None:
            label += f"\ncol: {node.column}"
        if node.valor is not None:
            label += f"\nvalor: {node.valor}"
        graph.node(str(node.id), label, style="filled", fillcolor='white')
        if node.padre:
            graph.edge(str(node.padre.id), str(node.id))
        for child in node.children:
            generar_nodos(child)
    generar_nodos(raiz)
    return graph

count = 0
def parser_sintactico_ll1(listtokens, table_ll1):
    global count
    error = False
    count = 0
    # Inicializar la pila con los símbolos iniciales
    node_PROGRAMA = Pila("NETCODE", False)
    node_dolar = Pila("$", True)
    stack = [node_PROGRAMA, node_dolar]
    nodoPadre = Arbol("NETCODE", None, None, None, False, node_PROGRAMA.id)
    listtokens_copy = list(listtokens)  # Copia de tokens para no modificar la lista original
    while True:
        if len(stack) == 0 or len(listtokens) == 0:
            error = True
            break
        if stack[0].simboloLex == "$" and listtokens[0].type == "$":
            break
        elif stack[0].es_terminal and stack[0].simboloLex == listtokens[0].type:
            stack.pop(0)
            listtokens.pop(0)
        elif stack[0].es_terminal and stack[0].simboloLex != listtokens[0].type:
            error = True
            break
        else:
            try:
                jiafei = table_ll1.loc[stack[0].simboloLex][listtokens[0].type]
            except KeyError:
                error = True
                break
            if jiafei == "e":
                padre_stack = stack.pop(0)
                padre = buscar(nodoPadre, padre_stack.id)
                nodo_e = Arbol("e", None, None, None, True, count)
                nodo_e.padre = padre
                padre.children.append(nodo_e)
                count += 1
            else:
                jiafei = jiafei.split(" ")
                padre_stack = stack.pop(0)
                padre = buscar(nodoPadre, padre_stack.id)
                for Symlexer in reversed(jiafei):
                    is_terminal = Symlexer in table_ll1.columns
                    node = Pila(Symlexer, is_terminal)
                    stack.insert(0, node)
                    nod = Arbol(Symlexer, None, None, None, is_terminal, node.id)
                    padre.children.insert(0, nod)
                    nod.padre = padre
                    if nod.es_terminal:
                        for token_actual in listtokens_copy:
                            if token_actual.type == nod.simbolo_lexer:
                                listtokens_copy.remove(token_actual)
                                break
    return (not error), nodoPadre if not error else None