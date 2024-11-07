import pandas as pd
from graphviz import Digraph

def generate_table_ll1(pathfile):
    df = pd.read_csv(pathfile, index_col = 0)
    df = df.fillna('')
    return df

class Node:
    def __init__(self, id, tipo, valor=None, linea=None, columna=None, terminal=False):
        self.id = id
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna
        self.terminal = terminal
        self.hijos = []
        self.padre = None 
    def añadir_hijo(self, hijo):
        hijo.padre = self  
        self.hijos.append(hijo)  
    def retornar_al_padre_netcode(self):
        nodo_actual = self
        while nodo_actual is not None and nodo_actual.tipo != "NETCODE":
            nodo_actual = nodo_actual.padre
        return nodo_actual
    
def buscar(node, id):
    if node.id == id:
        return node
    for hijo in node.hijos:
        found_node = buscar(hijo, id)
        if found_node is not None:
            return found_node
    return None

def recorrer_arbol_por_id(nodo):
    print(f"{nodo.id}, {nodo.tipo}, {nodo.valor}, {nodo.terminal}")
    for hijo in nodo.hijos:
        recorrer_arbol_por_id(hijo)

def arbolSintactico(raiz, contorno_hojas=False, opcion="tipo"):
    graph = Digraph()
    def generar_nodos(node):
        if opcion == "tipo":
            label = f"{node.tipo}"
        elif opcion == "linea":
            label = f"{node.linea}"
        elif opcion == "columna":
            label = f"{node.columna}"
        elif opcion == "valor":
            label = f"{node.valor}"
        elif opcion == "id":
            label = f"{node.id}"
        elif opcion == "terminal":
            label = f"{node.terminal}"
        else:
            label = f"{node.tipo}"
        if not node.hijos and contorno_hojas:
            graph.node(str(node.id), label, style="filled", fillcolor='lightgrey', peripheries='2')
        else:
            graph.node(str(node.id), label, style="filled", fillcolor='white')
        for hijo in node.hijos:
            graph.edge(str(node.id), str(hijo.id))
            generar_nodos(hijo)
    generar_nodos(raiz)
    return graph

def parser_sintactico_ll1(listatokens, parsing_table, inicial):
    stack = []
    count = 0
    node_dolar = Node(count, "$", "$", None, None, True)
    node_inicio = Node(count + 1, inicial, inicial, None, None, False)
    stack.append(node_dolar)
    stack.append(node_inicio)
    nodoPadre = node_inicio
    arbol = nodoPadre
    count += 2
    index = 0
    while stack:
        #print(f"{[s.tipo for s in stack]}")
        top = stack.pop()
        if top.terminal and index < len(listatokens) and listatokens[index].type == top.tipo:
            current_token = listatokens[index]
            top.valor = current_token.value
            top.linea = current_token.line
            top.columna = current_token.column
            index += 1
        elif top.terminal:
            return False, None
        elif top.tipo in parsing_table.index:
            if index < len(listatokens):
                current_token = listatokens[index].type
                try:
                    production = parsing_table.at[top.tipo, current_token]
                    if production:
                        if production == 'e':
                            nodo_e = Node(count, "e", "e", None, None, True)
                            top.añadir_hijo(nodo_e)
                            count += 1
                        else:
                            symbols = production.split()
                            nuevos_hijos = []
                            for symbol in symbols:  # Crear los nodos en el orden de aparición
                                is_terminal = symbol in [token.type for token in listatokens]
                                nodo_hijo = Node(count, symbol, None, None, None, is_terminal)
                                nuevos_hijos.append(nodo_hijo)
                                count += 1
                            for hijo in reversed(nuevos_hijos):
                                stack.append(hijo)
                            for hijo in nuevos_hijos:
                                top.añadir_hijo(hijo)
                    else:
                        return False, None
                except KeyError:
                    return False, None
            else:
                return False, None
        else:
            return False, None
    success = index == len(listatokens)
    if success:
        print("Análisis sintáctico exitoso: Se alcanzó el final de la pila.\n")
    return success, arbol if success else None