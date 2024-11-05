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
        print(f"Símbolo creado para main: {simbolo_main}")
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

# Función para buscar la definición de una función en el árbol, contar sus parámetros y procesar su cuerpo en INS
def buscar_y_verificar_parametros(funcionactual, node, tabla_de_simbolos):
    # Verificar si el nodo actual es FUNC y que tiene al menos 4 hijos
    if node.tipo == "FUNC" and len(node.hijos) > 3:
        # Verificar si el segundo hijo de FUNC tiene el valor funcionactual
        if node.hijos[1].valor == funcionactual:
            # Obtener el cuarto hijo, que es PARAMETROS
            parametros_node = node.hijos[3]
            # Contar los parámetros en el subárbol de PARAMETROS y verificar unicidad de IDs
            parametros_ids = contar_parametros(parametros_node)
            print(f"Número de parámetros encontrados para '{funcionactual}': {len(parametros_ids)}")
            
            # Recorrer el nodo INS de la función y verificar los IDs dentro
            for hijo in node.hijos:
                if hijo.tipo == "INS":
                    verificar_cuerpo_funcion(hijo, parametros_ids, funcionactual, tabla_de_simbolos)
            return len(parametros_ids)
    
    # Continuar buscando en todos los hijos en caso de no coincidencia
    for hijo in node.hijos:
        parametros_n = buscar_y_verificar_parametros(funcionactual, hijo, tabla_de_simbolos)
        if parametros_n > 0:  # Solo devolver si se encontró un resultado positivo
            return parametros_n
    return 0  # Retornar 0 si no se encuentra el nodo de la función

# Función auxiliar para contar el número de parámetros y verificar unicidad de IDs
def contar_parametros(param_node):
    unique_ids = set()  # Para verificar unicidad de IDs de parámetros
    
    # Función recursiva para contar conjuntos de VARIABLE ID TIPODATO
    def contar_nodos_parametro(node):
        # Verificar si el nodo actual tiene un conjunto completo de VARIABLE ID TIPODATO
        if node.tipo == "PARAMETROS" and len(node.hijos) >= 3:
            if node.hijos[0].tipo == "VARIABLE" and node.hijos[1].tipo == "ID" and node.hijos[2].tipo == "TIPODATO":
                parametro_id = node.hijos[1].valor
                # Verificar si el ID es único
                if parametro_id in unique_ids:
                    print(f"Error: El ID '{parametro_id}' ya existe en los parámetros.")
                else:
                    unique_ids.add(parametro_id)
        
        # Recursivamente buscar más parámetros en MASPARAMETROS
        for hijo in node.hijos:
            contar_nodos_parametro(hijo)
    
    # Iniciar el conteo desde el nodo PARAMETROS raíz
    contar_nodos_parametro(param_node)
    return unique_ids

# Función para verificar el cuerpo de la función en el nodo INS y crear símbolos para cada ID
def verificar_cuerpo_funcion(ins_node, parametros_ids, funcionactual, tabla_de_simbolos):
    for hijo in ins_node.hijos:
        # Caso 1: Verificar y crear un símbolo para cada ID en el cuerpo de la función
        if hijo.tipo == "ID":
            # Crear símbolo con ámbito del nombre de la función
            simbolo_id = Simbolo(lexema=hijo.valor, tipo_lexema=None, categoria="var", ambito=funcionactual)
            tabla_de_simbolos.append(simbolo_id)
            print(f"Símbolo creado en el ámbito '{funcionactual}': {simbolo_id}")

        # Caso 2: Verificar llamadas a funciones en el formato ID CORCHETEABI PAR CORCHETECERR, permitiendo varias instancias
        if hijo.tipo == "ID" and len(hijo.hijos) > 2 and hijo.hijos[1].tipo == "CORCHETEABI" and hijo.hijos[2].tipo == "PAR":
            id_funcion = hijo.valor
            if verificar(id_funcion, tabla_de_simbolos):
                print(f"Llamada de función verificada para '{id_funcion}' en el ámbito '{funcionactual}'.")

                # Procesar los parámetros en PAR
                procesar_parametros(hijo.hijos[2], tabla_de_simbolos, funcionactual)
            else:
                print(f"Error: La función '{id_funcion}' no está en la tabla de símbolos.")

        # Caso 3: Verificar si hay una operación entre llamadas de función
        if hijo.tipo == "OPERACION":
            print(f"Operación detectada en el ámbito '{funcionactual}'.")

        # Caso 4: VARIABLE ID TIPODATO IGUAL - Creación de variable dentro de la función
        if hijo.tipo == "VARIABLE" and len(hijo.hijos) > 2 and hijo.hijos[1].tipo == "ID" and hijo.hijos[2].tipo == "TIPODATO":
            id_variable = hijo.hijos[1].valor
            tipo_variable = hijo.hijos[2].valor
            simbolo_variable = Simbolo(lexema=id_variable, tipo_lexema=tipo_variable, categoria="var", ambito=funcionactual)
            tabla_de_simbolos.append(simbolo_variable)
            print(f"Símbolo creado para variable en el ámbito '{funcionactual}': {simbolo_variable}")

        # Caso 5: ID TIPODATO - Creación de variable sin asignación
        if hijo.tipo == "ID" and len(hijo.hijos) > 0 and hijo.hijos[1].tipo == "TIPODATO":
            id_variable = hijo.valor
            tipo_variable = hijo.hijos[1].valor
            simbolo_variable = Simbolo(lexema=id_variable, tipo_lexema=tipo_variable, categoria="var", ambito=funcionactual)
            tabla_de_simbolos.append(simbolo_variable)
            print(f"Símbolo creado para variable sin asignación en el ámbito '{funcionactual}': {simbolo_variable}")

        # Recursivamente verificar en los hijos
        verificar_cuerpo_funcion(hijo, parametros_ids, funcionactual, tabla_de_simbolos)

# Función auxiliar para procesar el nodo PAR en llamadas de función
def procesar_parametros(par_node, tabla_de_simbolos, ambito):
    # Contador de parámetros y verificación de llamadas anidadas
    num_parametros = 0
    
    for hijo in par_node.hijos:
        # Contar COMA para parámetros
        if hijo.tipo == "COMA":
            num_parametros += 1

        # Verificar llamadas de funciones anidadas
        elif hijo.tipo == "ID" and len(hijo.hijos) > 1 and hijo.hijos[1].tipo == "CORCHETEABI" and hijo.hijos[2].tipo == "PAR":
            id_anidado = hijo.valor
            if not verificar(id_anidado, tabla_de_simbolos):
                print(f"Error: El ID '{id_anidado}' en llamada anidada no está en la tabla de símbolos.")
            else:
                print(f"Llamada anidada de función verificada para '{id_anidado}' en el ámbito '{ambito}'.")

            # Recursivamente verificar los parámetros de la función anidada
            procesar_parametros(hijo.hijos[2], tabla_de_simbolos, id_anidado)

    # Número total de parámetros (número de COMA + 1)
    print(f"Número de parámetros en la llamada: {num_parametros + 1}")



















