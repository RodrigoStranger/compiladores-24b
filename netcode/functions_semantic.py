from functions_sintactic import Simbolo

def construir_tabla_de_simbolos(root_node):
    tabla_simbolos = []  # Tabla de símbolos como un vector (lista)

    def agregar_simbolo_a_tabla(simbolo):
        # Verificar si el símbolo ya existe en el mismo contexto (función)
        for s in tabla_simbolos:
            if s.nom_sym == simbolo.nom_sym and s.function == simbolo.function:
                print(f"Error: El símbolo '{simbolo.nom_sym}' ya existe en el contexto '{simbolo.function}'")
                return
        # Agregar símbolo a la tabla
        tabla_simbolos.append(simbolo)

    def recorrer_arbol(node, ambito="global"):
        # Omitir el nodo raíz si es de tipo NETCODE
        if node.simbolo_lexer == "NETCODE":
            for child in node.children:
                recorrer_arbol(child, ambito)
            return
        
        # Si el nodo representa una función (tipo FUNC), procesar el nombre y tipo de dato
        if node.simbolo_lexer == "FUNC":
            # Buscar el tipo en el nodo hijo de tipo OPDATO
            tipo_dato = None
            nombre_funcion = node.lexema

            for child in node.children:
                if child.simbolo_lexer == "OPDATO":
                    tipo_dato = child.tipo_data  # Tomamos el tipo de dato desde el nodo OPDATO
                    break

            # Agregar la función a la tabla de símbolos
            if tipo_dato:
                simbolo_funcion = Simbolo(tipo_data=tipo_dato, nom_sym=nombre_funcion, function=ambito, valor=None)
                simbolo_funcion.tipo_data = "function"  # Establecer el tipo como función
                agregar_simbolo_a_tabla(simbolo_funcion)
        
        # Agregar los símbolos del nodo actual a la tabla de símbolos
        for simbolo in node.simbolos:
            agregar_simbolo_a_tabla(simbolo)

        # Recorrer primero el hijo izquierdo, luego el derecho
        if node.children:
            if len(node.children) > 0:
                recorrer_arbol(node.children[0], ambito)  # Hijo izquierdo
            if len(node.children) > 1:
                recorrer_arbol(node.children[1], ambito)  # Hijo derecho

    # Iniciar el recorrido desde la raíz del árbol
    recorrer_arbol(root_node)
    return tabla_simbolos

