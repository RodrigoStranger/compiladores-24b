class Simbolo:
    def __init__(self, lexema, tipo_lexema, tipo, ambito):
        self.lexema = lexema
        self.tipo_lexema = tipo_lexema
        self.tipo = tipo
        self.ambito = ambito

    def __repr__(self):
        return f"Lexema: {self.lexema}, Tipo: {self.tipo_lexema}, Categoría: {self.tipo}, Ámbito: {self.ambito}"

# Verificar si un símbolo ya existe en el ámbito
def simbolo_existe(pila_simbolos, lexema, ambito):
    return any(simbolo.lexema == lexema and simbolo.ambito == ambito for simbolo in pila_simbolos)

# Recorrido preorden (RAIZ, IZQUIERDA, DERECHA) para construir la tabla de símbolos
def recorrer_preorden(node, pila_simbolos, ambito="global"):
    # Procesar el nodo actual según su tipo
    if node.tipo == "FUNC":
        procesar_funcion(node, pila_simbolos, ambito)
    elif node.tipo == "MAIN":
        procesar_main(node, pila_simbolos)
    elif node.tipo == "ASIG":
        procesar_asignacion(node, pila_simbolos, ambito)
    elif node.tipo == "ID" and node.hijos and node.hijos[0].tipo == "CORCHETEABI":
        validar_llamada_funcion(node, pila_simbolos)

    # Recorrer hijos de izquierda a derecha
    for hijo in node.hijos:
        recorrer_preorden(hijo, pila_simbolos, ambito)

# Función para procesar nodos FUNC y agregarlo a la tabla de símbolos
def procesar_funcion(node, pila_simbolos, ambito):
    funcion_id = next((hijo for hijo in node.hijos if hijo.tipo == "ID"), None)
    tipo_funcion = next((hijo.hijos[0].valor for hijo in node.hijos if hijo.tipo == "OPDATO" and hijo.hijos), None)
    if funcion_id and tipo_funcion:
        if not simbolo_existe(pila_simbolos, funcion_id.valor, ambito):
            pila_simbolos.append(Simbolo(funcion_id.valor, tipo_funcion, "function", ambito))
        
        # Nuevo ámbito dentro de la función
        nuevo_ambito = funcion_id.valor

        # Procesar parámetros
        parametros = next((hijo for hijo in node.hijos if hijo.tipo == "PARAMETROS"), None)
        if parametros:
            for param in parametros.hijos:
                if param.tipo == "VARIABLE":
                    var_id = next((h for h in param.hijos if h.tipo == "ID"), None)
                    var_tipo = next((h.hijos[0].valor for h in param.hijos if h.tipo == "TIPODATO" and h.hijos), None)
                    if var_id and var_tipo and not simbolo_existe(pila_simbolos, var_id.valor, nuevo_ambito):
                        pila_simbolos.append(Simbolo(var_id.valor, var_tipo, "var", nuevo_ambito))

        # Procesar instrucciones dentro de la función
        ins_nodo = next((hijo for hijo in node.hijos if hijo.tipo == "INS"), None)
        if ins_nodo:
            recorrer_preorden(ins_nodo, pila_simbolos, nuevo_ambito)

# Función para procesar el nodo MAIN y agregarlo a la tabla de símbolos
def procesar_main(node, pila_simbolos):
    main_tipo = next((hijo.hijos[0].valor for hijo in node.hijos if hijo.tipo == "TIPOENTERO" and hijo.hijos), None)
    if not simbolo_existe(pila_simbolos, "main", "global"):
        pila_simbolos.append(Simbolo("main", main_tipo, "function", "global"))

    # Procesar instrucciones dentro del MAIN
    ins_nodo = next((hijo for hijo in node.hijos if hijo.tipo == "INS"), None)
    if ins_nodo:
        recorrer_preorden(ins_nodo, pila_simbolos, ambito="main")

# Función para procesar nodos de asignación y agregar variables al ámbito correspondiente
def procesar_asignacion(node, pila_simbolos, ambito):
    var_id = next((hijo for hijo in node.hijos if hijo.tipo == "ID"), None)
    var_tipo = next((hijo.hijos[0].valor for hijo in node.hijos if hijo.tipo == "TIPODATO" and hijo.hijos), None)
    if var_id and var_tipo and not simbolo_existe(pila_simbolos, var_id.valor, ambito):
        pila_simbolos.append(Simbolo(var_id.valor, var_tipo, "var", ambito))

# Función para validar llamadas a funciones y asegurarse de que están declaradas
def validar_llamada_funcion(node, pila_simbolos):
    funcion_id = node.valor
    if not simbolo_existe(pila_simbolos, funcion_id, "global"):
        print(f"Error semántico: La función {funcion_id} no está declarada.")