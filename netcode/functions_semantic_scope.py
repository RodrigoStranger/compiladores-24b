from functions_semanctic import *

def verificar(lexema, tabla_de_simbolos):
    for simbolo in tabla_de_simbolos:
        if simbolo.lexema == lexema:
            return False
    return True

def verificar_asignado_valor(lexema, tabla_de_simbolos):
    for simbolo in tabla_de_simbolos:
        if simbolo.lexema == lexema:
            if simbolo.asignado_valor == False:
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

def verificar_par(id_lexema, list_par):
    for elemento in list_par:
        if elemento == id_lexema:
            return True
    return False

def verificar_ids_en_par(par_node, tabla_de_simbolos, errores, list_par):
    for hijo in par_node.hijos:
        if hijo.tipo == "ID":
            id_lexema = hijo.valor
            if not verificar_par(id_lexema, list_par):
                if verificar(id_lexema, tabla_de_simbolos):
                    descripcion_error = f"La variable {id_lexema} no está previamente declarada."
                    if not any(error.descripcion == descripcion_error for error in errores):
                        errores.append(Error(descripcion=descripcion_error))
            if verificar_asignado_valor(id_lexema, tabla_de_simbolos):
                descripcion_error = f"La variable {id_lexema} no tiene asignado ningún valor."
                if not any(error.descripcion == descripcion_error for error in errores):
                    errores.append(Error(descripcion=descripcion_error))
        else: verificar_ids_en_par(hijo, tabla_de_simbolos, errores, list_par)

def contar_hojas_par(node):
    cantidad = 0
    if not node.hijos:
        if node.tipo in ["ID", "DATO"]:
            cantidad += 1
    elif node.tipo == "DATO" and len(node.hijos) == 1:
        cantidad += 1
    else:
        for hijo in node.hijos:
            cantidad += contar_hojas_par(hijo)
    return cantidad

def contar_parametros(param_node, errores, funcionactual):
    unique_ids = set()
    def contar_nodos_parametro(node):
        if node.tipo == "PARAMETROS" and len(node.hijos) >= 3:
            if node.hijos[0].tipo == "VARIABLE" and node.hijos[1].tipo == "ID" and node.hijos[2].tipo == "TIPODATO":
                parametro_id = node.hijos[1].valor
                if parametro_id in unique_ids:
                    errores.append(Error(descripcion=f"Existe un parametro {parametro_id} duplicado en la función {funcionactual}."))
                else:
                    unique_ids.add(parametro_id)
        for hijo in node.hijos:
            contar_nodos_parametro(hijo)
    contar_nodos_parametro(param_node)
    return list(unique_ids)

def obtener_lista_parametros_por_nombre(nombre_funcion, root_node):
    unique_ids = set()
    nodo_netcode = root_node.retornar_al_padre_netcode()
    def buscar_nodo_funcion_por_nombre(node, nombre_buscado):
        if node.tipo == "FUNC" and len(node.hijos) > 1:
            if node.hijos[1].valor == nombre_buscado:
                return node
        for hijo in node.hijos:
            resultado = buscar_nodo_funcion_por_nombre(hijo, nombre_buscado)
            if resultado:
                return resultado
        return None
    func_node = buscar_nodo_funcion_por_nombre(nodo_netcode, nombre_funcion)
    if not func_node:
        return list(unique_ids)
    def contar_nodos_parametro(node):
        if node.tipo == "PARAMETROS" and len(node.hijos) >= 3:
            if node.hijos[0].tipo == "VARIABLE" and node.hijos[1].tipo == "ID" and node.hijos[2].tipo == "TIPODATO":
                parametro_id = node.hijos[1].valor
                unique_ids.add(parametro_id)
        for hijo in node.hijos:
            contar_nodos_parametro(hijo)
    if len(func_node.hijos) > 3:
        param_node = func_node.hijos[3]
        contar_nodos_parametro(param_node)
    return list(unique_ids)

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
        evaluar_asignaciones(node, tabla_de_simbolos, errores, "main")
    for hijo in node.hijos: recorrer_main(hijo, tabla_de_simbolos, errores)

def evaluar_asignaciones(node, tabla_de_simbolos, errores, ambitoactual):
    parametros_list = obtener_lista_parametros_por_nombre(ambitoactual, node)
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
                    if ambitoactual != "global":
                        for parametro in parametros_list:
                            if parametro == lexema: 
                                errores.append(Error(descripcion=f"La variable {lexema} ya está declarada en los parametros de la función {ambitoactual}"))
                            return
                    simbolo = Simbolo(lexema=lexema, tipo_lexema=tipo_lexema, categoria=categoria, ambito = ambitoactual)
                    simbolo.asignado_valor = False
                    tabla_de_simbolos.append(simbolo)
                else:
                    # recorrer EXPRESION tiene muchos hijos, incluso hay un MASEXPRESION que contiene EXPRESION
                    # en ello puede existir: ID / DATO / ID OPCION
                    # ID OPCION es como = ID CORCHETEABI PAR CORCHETECERR , osea una funcion
                    # en ID, se debe de verificar si existe ese ID en la tabla
                    # el DATO se omite
                    # cada EXPRESION esta separada por una OPERACION, asi que eso nos facilita la evaluacion.
                    print()
        # Verificar la estructura ID CORCHETEABI PAR CORCHETECERR
        if len(node.hijos) == 2:
            id_node = node.hijos[0]
            og_node = node.hijos[1]
            funcion_actual = id_node.valor
            if id_node.tipo == "ID" and og_node.tipo == "OG":
                if (len(og_node.hijos) == 3 and og_node.hijos[0].tipo == "CORCHETEABI" and og_node.hijos[1].tipo == "PAR" and og_node.hijos[2].tipo == "CORCHETECERR"):
                    if funcion_actual and not verificar(funcion_actual, tabla_de_simbolos):
                        par_node = og_node.hijos[1]
                        verificar_ids_en_par(par_node, tabla_de_simbolos, errores, parametros_list)
                        cantidad_parametros = contar_hojas_par(par_node)
                        nodo_netcode = node.retornar_al_padre_netcode()
                        buscar_y_verificar_parametros_y_cuerpo(funcion_actual, cantidad_parametros, nodo_netcode, tabla_de_simbolos, errores)
                    else : errores.append(Error(descripcion=f"La función {funcion_actual} no esta declarada.")) 
        # Verificar la estructura ID = COSAS...............
        #           
    for hijo in node.hijos: evaluar_asignaciones(hijo, tabla_de_simbolos, errores, ambitoactual)

def buscar_y_verificar_parametros_y_cuerpo(funcionactual, cantidadparametros, node, tabla_de_simbolos, errores):
    if node.tipo == "FUNC" and len(node.hijos) > 3:
        if node.hijos[1].valor == funcionactual:
            parametros_node = node.hijos[3]
            parametros_ids = contar_parametros(parametros_node, errores, funcionactual)
            if len(parametros_ids) != cantidadparametros:
                errores.append(Error(descripcion=f"Existe una desigualdad de parametros en {funcionactual}."))
                return
            evaluar_asignaciones(node, tabla_de_simbolos, errores, funcionactual)
    for hijo in node.hijos: buscar_y_verificar_parametros_y_cuerpo(funcionactual, cantidadparametros, hijo, tabla_de_simbolos, errores)