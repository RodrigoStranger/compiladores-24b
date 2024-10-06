import os
import math

from lexic import listtokens
from functions_sintactic import generate_table_ll1
from graphviz import Digraph

count = 1 

directory2 = os.path.dirname(__file__)
sketchfile = 'table_ll1.csv'
pathfile2 = os.path.join(directory2, '..', 'table_ll1', sketchfile)

table_ll1 = generate_table_ll1(pathfile2)

class Simbolo:
    def __init__(self, tipo_data, nom_sym, function, valor=None):
        self.tipo_data = tipo_data
        self.nom_sym = nom_sym
        self.function = function
        self.valor = valor

class Arbol:
    def __init__(self, simbolo_lexer, lexema, line, column, es_terminal, id, tipo_data=None, valor=None):
        global count
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


node_PROGRAMA = Pila("NETCODE", False)
node_dolar = Pila("$", True)
stack = [node_PROGRAMA, node_dolar]
nodo_actual = 1
nodoPadre = Arbol("NETCODE", None, None, None, False, node_PROGRAMA.id)

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

error = False
listtokens_copy = []

for token_actual in listtokens:
    listtokens_copy.append(token_actual)

while True:
    if len(stack) == 0 or len(listtokens) == 0:
        error = True
        break
    if stack[0].simboloLex == "$" and listtokens[0].type == "$":
        break
    elif stack[0].es_terminal and stack[0].simboloLex == listtokens[0].type:
        stack.pop(0)
        token = listtokens.pop(0)
        tipo_data = listtokens[0].type if listtokens else None
        if tipo_data is not None:
            padre = buscar(nodoPadre, nodo_actual)
            padre.tipo_data = tipo_data

    elif stack[0].es_terminal and stack[0].simboloLex != listtokens[0].type:
        error = True
        break
    else:
        jiafei = table_ll1.loc[stack[0].simboloLex][listtokens[0].type]
        if jiafei == "e":
            padre_stack = stack.pop(0)
            padre = buscar(nodoPadre, padre_stack.id)
            # Crear un nodo para "e" y agregarlo como hijo del padre actual
            nodo_e = Arbol("e", None, None, None, True, count)
            nodo_e.padre = padre
            padre.children.append(nodo_e)  # Aquí agregamos correctamente el nodo "e"
            # Avanzar el contador de nodos
            count += 1
        else:
            if isinstance(jiafei, float) and math.isnan(jiafei):
                error = True
                break
            else:
                jiafei = jiafei.split(" ")
                padre_stack = stack.pop(0)
                padre = buscar(nodoPadre, padre_stack.id)
                for Symlexer in jiafei[::-1]:
                    is_terminal = Symlexer in table_ll1.columns
                    node = Pila(Symlexer, is_terminal)
                    stack.insert(0, node)
                    nodo_actual = node.id
                    nod = Arbol(Symlexer, None, None, None, is_terminal, node.id)
                    padre.children.insert(0, nod)
                    nod.padre = padre
                    if nod.es_terminal:
                        for token_actual in listtokens_copy:
                            if token_actual.type == nod.simbolo_lexer:
                                listtokens_copy.remove(token_actual)
                                break

if not error:
    graph = arbolSintactico(nodoPadre)
    output_folder = 'tree'
    if not os.path.exists(output_folder): os.makedirs(output_folder)
    output_pdf_path = os.path.join(output_folder, 'tree_sintactic') 
    graph.render(output_pdf_path, format='png', view=True)
