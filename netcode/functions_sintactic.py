import pandas as pd
import matplotlib.pyplot as plt
from graphviz import Digraph
import math
from functions_lexic import Token

#funcion que genera una tabla ll1 
def generate_table_ll1(pathfile):
    df = pd.read_csv(pathfile, index_col = 0)
    df = df.fillna('')
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
def ll1_parse(listatokens, parsing_table):
    stack = ['$','NETCODE']
    index = 0
    while stack:
        print(f"Estado de la pila: {stack}, Tokens restantes: {[token.type for token in listatokens[index:]]}")
        top = stack.pop()
        # si el símbolo en la cima es un terminal
        if top in [token.type for token in listatokens]:
            if index < len(listatokens) and listatokens[index].type == top:
                print(f"Coincidencia encontrada: {top}")
                index += 1
            else:
                print("\nError: Se esperaba '{}' pero se encontró '{}'".format(
                    top, listatokens[index].type if index < len(listatokens) else 'fin de entrada'))
                print("Lista de tokens restantes: ", [token.type for token in listatokens[index:]])
                return False
        # si el símbolo en la cima es un no terminal
        elif top in parsing_table.index:
            if index < len(listatokens):
                current_token = listatokens[index].type
                try:
                    production = parsing_table.at[top, current_token]
                    if production != '':
                        # descomponer la producción y añadir al stack
                        if production != 'e':  # 'e' representa la producción vacía
                            print(f"Producción encontrada para {top}: {production}")
                            stack.extend(reversed(production.split()))  # añadir en orden inverso
                        else:
                            print(f"Producción vacía encontrada para {top}")
                    else:
                        print("\nError: No hay producción válida para el no terminal '{}' con el token '{}'".format(
                            top, current_token))
                        print("Lista de tokens restantes: ", [token.type for token in listatokens[index:]])
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
            print("Lista de tokens restantes: ", [token.type for token in listatokens[index:]])
            return False
    # verifica si se ha consumido toda la entrada
    success = index == len(listatokens)
    if success:
        print("\nAnálisis exitoso.")
    else:
        print("\nFalló el análisis. Se esperaban más tokens pero la entrada se terminó.")
        print("Lista de tokens restantes: ", [token.type for token in listatokens[index:]])
    return success

class Simbolo:
    def __init__(self, tipo_data, nom_sym, function, valor=None):
        self.tipo_data = tipo_data  # Tipo de dato del símbolo (e.g., int, float, string)
        self.nom_sym = nom_sym      # Nombre del símbolo
        self.function = function    # Contexto o función donde se define el símbolo
        self.valor = valor          # Valor asignado al símbolo (si lo tiene)

class Node:
    def __init__(self, simbolo_lexer, lexema, line, column, es_terminal, id, tipo_data=None, valor=None):
        self.id = id                        # Identificador único del nodo
        self.lexema = lexema                # Lexema asociado al nodo
        self.simbolo_lexer = simbolo_lexer  # Tipo de símbolo del analizador léxico (e.g., identificador, palabra clave)
        self.es_terminal = es_terminal      # Booleano que indica si es un nodo terminal
        self.line = line                    # Línea en la que se encuentra el símbolo en el código fuente
        self.column = column                # Columna donde comienza el símbolo en el código fuente
        self.children = []                  # Lista de nodos hijos
        self.padre = None                   # Nodo padre (para referencia en el árbol)
        self.simbolos = []                  # Lista de símbolos definidos en este nodo
        self.tipo_data = tipo_data          # Tipo de dato asociado (para análisis semántico)
        self.valor = valor                  # Valor asociado al nodo (si lo tiene)

    def add_child(self, child):
        self.children.append(child)
        child.padre = self  # Establecer al nodo actual como padre del hijo

    def agregar_simbolo(self, tipo_data, nom_sym, function, valor=None):
        simbolo = Simbolo(tipo_data, nom_sym, function, valor=valor)
        self.simbolos.append(simbolo)
        # Actualizar el tipo de dato y el valor del nodo si corresponde a un símbolo
        self.tipo_data = tipo_data
        self.valor = valor

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

def arbolSintacticoContorno(raiz):
    graph = Digraph()
    def generar_nodos(node):
        label = f"{node.simbolo_lexer}"
        if node.line is not None:
            label += f"\nline: {node.line}"
        if node.column is not None:
            label += f"\ncol: {node.column}"
        if node.valor is not None:
            label += f"\nvalor: {node.valor}"
        # Si es una hoja (no tiene hijos), le aplicamos doble contorno
        if not node.children:
            graph.node(str(node.id), label, style="filled", fillcolor='white', peripheries='2')
        else:
            graph.node(str(node.id), label, style="filled", fillcolor='white')
        if node.padre:
            graph.edge(str(node.padre.id), str(node.id))
        for child in node.children:
            generar_nodos(child)
    generar_nodos(raiz)
    return graph

def parser_sintactico_ll1(listtokens, table_ll1, inicial):
    global count
    error = False
    count = 0
    # Inicializar la pila con los símbolos iniciales
    node_PROGRAMA = Node(inicial, inicial, None, None, False, count)
    node_dolar = Node("$", "$", None, None, True, count + 1)
    stack = [node_PROGRAMA, node_dolar]
    nodoPadre = node_PROGRAMA
    listtokens_copy = list(listtokens)  # Copia de tokens para no modificar la lista original
    count += 2
    while True:
        print(f"Estado de la pila: {[s.simbolo_lexer for s in stack]}")
        print(f"Tokens restantes: {[token.type for token in listtokens]}")
        if len(stack) == 0 or len(listtokens) == 0:
            error = True
            print("Error: Pila vacía o lista de tokens vacía antes de tiempo.")
            break
        if stack[0].simbolo_lexer == "$" and listtokens[0].type == "$":
            print(" ")
            print("Análisis exitoso: Se alcanzó el símbolo de fin de entrada.")
            break
        elif stack[0].es_terminal and stack[0].simbolo_lexer == listtokens[0].type:
            print(f"Coincidencia encontrada: {stack[0].simbolo_lexer}")
            stack.pop(0)
            listtokens.pop(0)
            print(" ")
        elif stack[0].es_terminal and stack[0].simbolo_lexer != listtokens[0].type:
            error = True
            print(f"Error: Se esperaba '{stack[0].simbolo_lexer}', pero se encontró '{listtokens[0].type}'.")
            break
        else:
            try:
                production = table_ll1.loc[stack[0].simbolo_lexer][listtokens[0].type]
                print(f"Producción encontrada para {stack[0].simbolo_lexer}: {production}")
                print(" ")
            except KeyError:
                error = True
                print(f"Error: No hay producción válida para el no terminal '{stack[0].simbolo_lexer}' con el token '{listtokens[0].type}'.")
                break
            if production == "e":
                print(f"Producción vacía aplicada para {stack[0].simbolo_lexer}")
                padre_stack = stack.pop(0)
                padre = buscar(nodoPadre, padre_stack.id)
                nodo_e = Node("e", "e", None, None, True, count)
                nodo_e.padre = padre
                padre.add_child(nodo_e)
                count += 1
                print(" ")
            else:
                symbols = production.split(" ")
                padre_stack = stack.pop(0)
                padre = buscar(nodoPadre, padre_stack.id)
                for Symlexer in reversed(symbols):
                    if Symlexer:  # Evitar agregar símbolos vacíos
                        is_terminal = Symlexer in table_ll1.columns
                        node = Node(Symlexer, Symlexer, None, None, is_terminal, count)
                        count += 1
                        stack.insert(0, node)
                        padre.children.insert(0, node)
                        node.padre = padre
                        if node.es_terminal:
                            for token_actual in listtokens_copy:
                                if token_actual.type == node.simbolo_lexer:
                                    listtokens_copy.remove(token_actual)
                                    break
    return (not error), nodoPadre if not error else None