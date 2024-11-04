import pandas as pd
import matplotlib.pyplot as plt
from graphviz import Digraph

def generate_table_ll1(pathfile):
    df = pd.read_csv(pathfile, index_col = 0)
    df = df.fillna('')
    return df

class Node:
    def __init__(self, id, tipo, valor, linea, columna, terminal):
        self.id = id                  # Identificador único del nodo
        self.tipo = tipo              # Tipo del token (para búsqueda en la tabla)
        self.valor = valor            # Valor del token
        self.linea = linea            # Línea en la que se encuentra el token
        self.columna = columna        # Columna en la que se encuentra el token
        self.hijos = []               # Lista de hijos del nodo
        self.terminal = terminal      # Booleano que indica si es un nodo terminal (hoja)
        self.padre = None             # Referencia al nodo padre

    def añadir_hijo(self, hijo):
        self.hijos.append(hijo)
        hijo.padre = self  # Establece el nodo actual como padre del hijo

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
        # Seleccionar el valor de la etiqueta en función de la opción proporcionada
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
        else:
            label = f"{node.tipo}"
        '''
        if node.linea is not None:
            label += f"\nline: {node.linea}"
        if node.columna is not None:
            label += f"\ncol: {node.columna}"
        if node.valor is not None:
            label += f"\nvalor: {node.valor}"
        '''
        # Aplicar doble contorno si es hoja y `contorno_hojas` es True
        if not node.hijos and contorno_hojas:
            graph.node(str(node.id), label, style="filled", fillcolor='white', peripheries='2')
        else:
            graph.node(str(node.id), label, style="filled", fillcolor='white')
        # Conectar con el nodo padre
        if node.padre:
            graph.edge(str(node.padre.id), str(node.id))
        # Llamada recursiva para cada hijo
        for hijo in node.hijos:
            generar_nodos(hijo)
    generar_nodos(raiz)
    return graph

def parser_sintactico_ll1(listtokens, table_ll1, inicial):
    global count
    error = False
    count = 0
    # Nodo inicial y nodo de fin de entrada
    node_PROGRAMA = Node(count, inicial, inicial, None, None, False)
    node_dolar = Node(None, "$", "$", None, None, True)
    stack = [node_dolar, node_PROGRAMA]  # Pila con el símbolo inicial y el fin de entrada
    nodoPadre = node_PROGRAMA
    listtokens_copy = list(listtokens)  # Copia de tokens para preservar la lista original
    count += 1
    while stack and listtokens:  # Mientras haya elementos en la pila y tokens
        #print(f"Stack: {[s.tipo for s in stack]}")
        top_stack = stack.pop()  # Extraemos el símbolo del tope de la pila
        # Si alcanzamos el fin de entrada tanto en la pila como en los tokens
        if top_stack.tipo == "$" and listtokens[0].type == "$":
            print("Análisis sintáctico exitoso: Se alcanzó el símbolo de fin de entrada de la pila.\n")
            break
        # Coincidencia directa entre el terminal en la pila y el primer token
        elif top_stack.terminal and top_stack.tipo == listtokens[0].type:
            current_token = listtokens.pop(0)  # Sacar el token de la lista
            top_stack.valor = current_token.value  # Asignar valor, línea y columna al nodo
            top_stack.linea = current_token.line
            top_stack.columna = current_token.column
        # Error de coincidencia entre el terminal y el token actual
        elif top_stack.terminal and top_stack.tipo != listtokens[0].type:
            print("Error")
            error = True
            break
        # Expansión del no terminal
        else:
            try:
                # Obtener la producción desde la tabla LL(1)
                production = table_ll1.loc[top_stack.tipo][listtokens[0].type]
            except KeyError:
                error = True
                print("Error")
                break
            # Si la producción es "e" (vacía)
            if production == "e":
                padre = buscar(nodoPadre, top_stack.id)
                nodo_e = Node(count, "e", "e", None, None, True)
                padre.añadir_hijo(nodo_e)
                count += 1
            # Producción no vacía: Expansión de nodos
            else:
                symbols = production.split(" ")  # Dividir producción en símbolos
                padre = buscar(nodoPadre, top_stack.id)
                # Crear nodos hijos para la producción en orden de aparición
                nuevos_hijos = []
                for Symlexer in symbols:
                    if Symlexer:  # Evitar símbolos vacíos
                        is_terminal = Symlexer in table_ll1.columns
                        value = Symlexer if not is_terminal else None  # Asignar tipo como valor si es no terminal
                        line, column = (None, None)
                        # Extraer datos del token si es terminal
                        if is_terminal:
                            for token_actual in listtokens_copy:
                                if token_actual.type == Symlexer:
                                    value = token_actual.value
                                    line = token_actual.line
                                    column = token_actual.column
                                    listtokens_copy.remove(token_actual)
                                    break
                        # Crear nodo hijo y agregarlo en orden
                        node = Node(count, Symlexer, value, line, column, is_terminal)
                        count += 1
                        nuevos_hijos.append(node)
                # Agregar nodos hijos al nodo padre en orden natural
                for hijo in nuevos_hijos:
                    padre.añadir_hijo(hijo)
                # Insertar los nodos hijos en la pila en orden inverso para preservar el orden natural
                for hijo in reversed(nuevos_hijos):
                    stack.append(hijo)
    return (not error), nodoPadre if not error else None