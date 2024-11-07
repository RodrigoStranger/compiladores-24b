class Simbolo:
    def __init__(self, lexema, tipo_lexema, categoria, ambito):
        self.lexema = lexema
        self.tipo_lexema = tipo_lexema
        self.categoria = categoria
        self.ambito = ambito
    def __repr__(self): return f"{self.lexema}, {self.tipo_lexema}, {self.categoria}, {self.ambito}"

class Error:
    def __init__(self, descripcion):
        self.descripcion = descripcion
    def __repr__(self): return f"{self.descripcion}"

def imprimir_resultado_errores(errores_semanticos):
    if not errores_semanticos:
        print("\nAnálisis semántico exitoso")
        return
    print("\nErrores encontrados:")
    for error in errores_semanticos:
        print(error) 

def imprimir_tabla_de_simbolos(tabla_de_simbolos):
    print("Tabla de Símbolos:")
    for simbolo in tabla_de_simbolos:
        print(simbolo)

def verificar(lexema, tabla_de_simbolos):
    for simbolo in tabla_de_simbolos:
        if simbolo.lexema == lexema:
            return False
    return True

def obtener_valor_hoja(node):
    if not node.hijos:
        return node.valor
    for hijo in node.hijos:
        valor = obtener_valor_hoja(hijo)
        if valor is not None:
            return valor
    return None

def contiene_retorno(node):
    if node.tipo == "RETORNAR":
        return True
    for hijo in node.hijos:
        if contiene_retorno(hijo):
            return True
    return False

def contar(node, valor):
    count = 0
    if node.tipo == valor:
        count += 1
    for hijo in node.hijos:
        count += contar(hijo, valor)
    return count

def recorrer_funciones(node, tabla_de_simbolos, errores):
    if node.tipo == "FUNC":
        tipo = None
        lexema = None
        for hijo in node.hijos:
            if hijo.tipo == "OPDATO":
                tipo = obtener_valor_hoja(hijo)
            elif hijo.tipo == "ID":
                lexema = hijo.valor
        if lexema and not verificar(lexema, tabla_de_simbolos):
            errores.append(Error(descripcion = f"Ya existe una función {lexema} definida."))
            return
        num_retorno = 0
        for hijo in node.hijos:
            if hijo.tipo == "INS":
                num_retorno += contar(hijo, "RETORNAR")
        if tipo == "void":
            if num_retorno > 0:
                errores.append(Error(descripcion = f"{lexema} es una función de tipo void y no debe contener echo."))
        else:
            if num_retorno == 0:
                errores.append(Error(descripcion = f"La función {lexema} debe retornar algo."))
        simbolo = Simbolo(lexema = lexema, tipo_lexema = tipo, categoria = "function", ambito = "global")
        tabla_de_simbolos.append(simbolo)
        return
    for hijo in node.hijos: recorrer_funciones(hijo, tabla_de_simbolos, errores)

def recorrer_main(node, tabla_de_simbolos, errores):
    if node.tipo == "MAIN":
        lexema = node.hijos[1].valor if len(node.hijos) > 1 else None
        tipo_lexema = node.hijos[2].valor if len(node.hijos) > 2 else None
        simbolo_main = Simbolo(lexema = lexema, tipo_lexema = tipo_lexema, categoria = "function", ambito = "global")
        tabla_de_simbolos.append(simbolo_main)
        evaluar_asignaciones(node, tabla_de_simbolos, errores)
    for hijo in node.hijos: recorrer_main(hijo, tabla_de_simbolos, errores)

def evaluar_asignaciones(node, tabla_de_simbolos, errores):
    if node.tipo == "ASIG":
        # Verificar la estructura VARIABLE ID TIPODATO OPC
        if len(node.hijos) == 4:
            variable = node.hijos[0]
            id_node = node.hijos[1]
            tipo_dato = node.hijos[2]
            opc_node = node.hijos[3]
            if (variable.tipo == "VARIABLE" and id_node.tipo == "ID" and tipo_dato.tipo == "TIPODATO" and opc_node.tipo == "OPC"):
                if len(opc_node.hijos) == 1 and opc_node.hijos[0].valor == "e":
                    lexema = id_node.valor
                    tipo_lexema = obtener_valor_hoja(tipo_dato)
                    categoria = variable.valor
                    if lexema and not verificar(lexema, tabla_de_simbolos):
                        errores.append(Error(descripcion=f"Ya existe una variable {lexema} definida."))
                        return
                    simbolo = Simbolo(lexema=lexema, tipo_lexema=tipo_lexema, categoria=categoria, ambito="main")
                    tabla_de_simbolos.append(simbolo)
        # Verificar la estructura ID CORCHETEABI PAR CORCHETECERR
        if len(node.hijos) == 2:
            id_node = node.hijos[0]
            og_node = node.hijos[1]
            funcion_actual = id_node.valor
            if id_node.tipo == "ID" and og_node.tipo == "OG":
                if (len(og_node.hijos) == 3 and og_node.hijos[0].tipo == "CORCHETEABI" and og_node.hijos[1].tipo == "PAR" and og_node.hijos[2].tipo == "CORCHETECERR"):
                    if funcion_actual and not verificar(funcion_actual, tabla_de_simbolos):
                        print("Función vacía encontrada") 
                        #verificar dentro de PAR (ID) esten declarados previamente osea que esten en la tabla de simbolos,
                        par_node = og_node.hijos[1]
                        verificar_ids_en_par(par_node, tabla_de_simbolos, errores)
                        #obtener la cantidad de parametros 
                        cantidad_parametros = contar_hojas_par(par_node)
                        print(f"Número de parámetros encontrados: {cantidad_parametros}")

                        
    for hijo in node.hijos: evaluar_asignaciones(hijo, tabla_de_simbolos, errores)

def verificar_ids_en_par(par_node, tabla_de_simbolos, errores):
    for hijo in par_node.hijos:
        if hijo.tipo == "ID":
            id_lexema = hijo.valor
            if verificar(id_lexema, tabla_de_simbolos):
                errores.append(Error(descripcion=f"{id_lexema} no está previamente declarado"))
        else: verificar_ids_en_par(hijo, tabla_de_simbolos, errores)


def contar_hojas_par(node):
    cantidad = 0
    if not node.hijos:  # Si el nodo es una hoja
        if node.tipo in ["ID", "DATO"]:
            cantidad += 1
    elif node.tipo == "DATO" and len(node.hijos) == 1:
        # Si el nodo es DATO y tiene una hoja, contar esa hoja
        cantidad += 1
    else:
        # Recursivamente contar las hojas en los hijos
        for hijo in node.hijos:
            cantidad += contar_hojas_par(hijo)
    return cantidad





















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



















