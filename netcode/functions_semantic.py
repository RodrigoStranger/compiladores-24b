class Simbolo:
    def __init__(self, lexema, tipo_lexema, categoria, ambito):
        self.lexema = lexema
        self.tipo_lexema = tipo_lexema
        self.tipo = categoria
        self.ambito = ambito

    def __repr__(self): return f"{self.lexema}, {self.tipo_lexema}, {self.tipo}, {self.ambito}"

def preorder(node):
    if not node.hijos:
        if node.valor != "e":
            print(node.valor)
        return
    for hijo in node.hijos:
        preorder(hijo)

def preorder_tipo(node):
    print(node.tipo)
    for hijo in node.hijos:
        preorder_tipo(hijo)

def verificar(lexema, tabla_de_simbolos):
    for simbolo in tabla_de_simbolos:
        if simbolo.lexema == lexema:
            return False
    return True

def obtener_valor_hoja(node):
    # Recorrer hasta la hoja y devolver el valor
    if not node.hijos:
        return node.valor
    for hijo in node.hijos:
        valor = obtener_valor_hoja(hijo)
        if valor is not None:
            return valor
    return None

def contiene_retorno(node):
    # Verificar si el nodo actual es RETORNAR
    if node.tipo == "RETORNAR":
        return True
    # Recorrer los hijos en busca de RETORNAR
    for hijo in node.hijos:
        if contiene_retorno(hijo):
            return True
    return False

def crear_simbolo_func(node, tabla_de_simbolos):
    if node.tipo == "FUNC":
        tipo = None
        # Obtener el tipo de la función desde el nodo OPDATO
        for hijo in node.hijos:
            if hijo.tipo == "OPDATO":
                tipo = obtener_valor_hoja(hijo)
                break

        # Obtener el lexema de la función (nombre de la función)
        lexema = node.hijos[1].valor if len(node.hijos) > 1 else None

        # Si el tipo de la función es void, verificar que no haya un nodo RETORNAR en INS
        if tipo == "void":
            for hijo in node.hijos:
                if hijo.tipo == "INS":
                    if contiene_retorno(hijo):
                        print(f"Error: La función '{lexema}' es de tipo 'void' y no debe contener un 'RETORNAR'.")
                        return False  # Terminar si hay un error, sin agregar el símbolo

        # Verificar si la función ya existe en la tabla de símbolos
        if lexema and verificar(lexema, tabla_de_simbolos):
            # Crear y agregar el símbolo de la función
            simbolo = Simbolo(lexema=lexema, tipo_lexema=tipo, categoria="function", ambito="global")
            tabla_de_simbolos.append(simbolo)
            print(f"Símbolo creado: {simbolo}")
        else:
            print(f"Ya existe la función '{lexema}' en la tabla de símbolos.")
        return False

    # Recorrer recursivamente los hijos en busca de nodos FUNC adicionales
    for hijo in node.hijos:
        crear_simbolo_func(hijo, tabla_de_simbolos)

def procesar_main(node, tabla_de_simbolos):
    # Buscar el nodo MAIN y crear su símbolo
    if node.tipo == "MAIN":
        # Crear símbolo para MAIN
        lexema = node.hijos[1].valor if len(node.hijos) > 1 else None
        tipo_lexema = node.hijos[2].valor if len(node.hijos) > 2 else None
        simbolo_main = Simbolo(lexema=lexema, tipo_lexema=tipo_lexema, categoria="function", ambito="global")
        tabla_de_simbolos.append(simbolo_main)
        print(f"Símbolo creado para MAIN: {simbolo_main}")
        # Procesar todos los nodos de INS en busca de ASIG
        for hijo in node.hijos:
            if hijo.tipo == "INS":
                procesar_asignaciones(hijo, tabla_de_simbolos)
        return  # Terminar la búsqueda después de procesar MAIN
    # Recorrer recursivamente los hijos para encontrar MAIN
    for hijo in node.hijos:
        procesar_main(hijo, tabla_de_simbolos)

def procesar_asignaciones(node, tabla_de_simbolos):
    # Recorrer exhaustivamente el subárbol INS en busca de nodos ASIG
    if node.tipo == "ASIG":
        # Comprobar si ASIG tiene un hijo VARIABLE, indicando asignación
        tiene_variable = any(sub_hijo.tipo == "VARIABLE" for sub_hijo in node.hijos)
        if tiene_variable:
            # Obtener el lexema del segundo hijo de ASIG
            lexema = node.hijos[1].valor if len(node.hijos) > 1 else None
            # Obtener el tipo de lexema desde la hoja del tercer hijo
            tipo_lexema = obtener_valor_hoja(node.hijos[2]) if len(node.hijos) > 2 else None
            # Verificar si el símbolo ya existe en la tabla de símbolos
            if lexema and verificar(lexema, tabla_de_simbolos):
                # Crear símbolo para la variable y agregarlo a la tabla de símbolos
                simbolo = Simbolo(lexema=lexema, tipo_lexema=tipo_lexema, categoria="var", ambito="main")
                tabla_de_simbolos.append(simbolo)
                print(f"Símbolo creado para asignación: {simbolo}")
            else:
                print(f"La variable '{lexema}' ya existe en la tabla de símbolos.")
        else:
            # No existe VARIABLE, verificar si el primer hijo (ID) tiene un valor que coincide en la tabla
            id_valor = node.hijos[0].valor if len(node.hijos) > 0 else None
            if id_valor and any(simbolo.lexema == id_valor for simbolo in tabla_de_simbolos):
                print(f"Llamada verificada: {id_valor} ya existe en la tabla de símbolos.")
            else: print(f"{id_valor} no existe en la tabla de símbolos.")
    # Recursivamente recorrer todos los hijos para encontrar ASIG dentro de INS
    for hijo in node.hijos:
        procesar_asignaciones(hijo, tabla_de_simbolos)
