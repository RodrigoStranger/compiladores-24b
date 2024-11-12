class Simbolo:
    def __init__(self, lexema, tipo_lexema, categoria, ambito):
        self.lexema = lexema
        self.tipo_lexema = tipo_lexema
        self.categoria = categoria
        self.ambito = ambito
        self.asignado_valor = None
    def __repr__(self): return f"{self.lexema}, {self.tipo_lexema}, {self.categoria}, {self.ambito}"

def eliminar_simbolos_por_ambito(ambitoactual, tabla_de_simbolos):
    for i in range(len(tabla_de_simbolos) - 1, -1, -1):
        if tabla_de_simbolos[i].ambito == ambitoactual:
            del tabla_de_simbolos[i]

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