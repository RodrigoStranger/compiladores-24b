from lexic import listtokens
from functions_sintactic import generate_table_ll1
from functions_lexic import Token
from functions_sintactic import generate_token_example
import os
from graphviz import Digraph
import math

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
    def __init__(self, simbolo_lexer, lexema, line, column, scotty, id, tipo_data=None, valor=None):
        global count
        self.id = id
        self.lexema = lexema
        self.simbolo_lexer = simbolo_lexer
        self.scotty = scotty
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
    def __init__(self, hachico, scotty):
        global count
        self.id = count
        self.simboloLex = hachico
        self.scotty = scotty
        count += 1

class SimboloManager:
    def __init__(self):
        self.simbolos = []
    def insert(self, simbolo_lexer):
        self.simbolos.append(simbolo_lexer)
    def lookup(self, nom_sym):
        for simbolo_lexer in self.simbolos:
            if simbolo_lexer.nom_sym == nom_sym:
                return simbolo_lexer
        return None

generate_token_example("$", listtokens)

Token = listtokens
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
t = []

for token_actual in Token:
    t.append(token_actual)

while True:
    if len(stack) == 0 or len(Token) == 0:
        print("\n--- ERROR SINTÁCTICO: PILA O LISTA DE TOKENS VACÍA ---\n")
        error = True
        break

    if stack[0].simboloLex == "$" and Token[0].type == "$":
        break

    elif stack[0].scotty and stack[0].simboloLex == Token[0].type:
        stack.pop(0)
        token = Token.pop(0)
        tipo_data = Token[0].type if Token else None
        if tipo_data is not None:
            padre = buscar(nodoPadre, nodo_actual)
            padre.tipo_data = tipo_data

    elif stack[0].scotty and stack[0].simboloLex != Token[0].type:
        print("\n--- ERROR SINTÁCTICO DETECTADO ---\n")
        error = True
        break
    else:
        jiafei = table_ll1.loc[stack[0].simboloLex][Token[0].type]
        if jiafei == "e":
            stack.pop(0)
        else:
            if isinstance(jiafei, float) and math.isnan(jiafei):
                print("\n--- ERROR SINTÁCTICO DETECTADO ---\n")
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

                    if nod.scotty:
                        for token_actual in t:
                            if token_actual.type == nod.simbolo_lexer:
                                nod.valor = token_actual.value
                                nod.line = token_actual.line
                                t.remove(token_actual)
                                break

if not error:
    graph = arbolSintactico(nodoPadre)
    graph.render('arbolSintactico', format='png', view=True)
