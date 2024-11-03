class Simbolo:
    def __init__(self, lexema, tipo_lexema, tipo, ambito):
        self.lexema = lexema  # se extrae del Node.valor
        self.tipo_lexema = tipo_lexema  # se extrae del id del lexema + 1 -> valor
        self.tipo = tipo  # var, function
        self.ambito = ambito  # global o la función a la que pertenece

# Crear lista para almacenar los símbolos
tabla_simbolos = []
