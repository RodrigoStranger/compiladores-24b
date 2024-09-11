import ply.yacc as yacc
from lexer import listtokens
from lexer import data



# Crear el parser
parser = yacc.yacc()


# Analizar los datos de ejemplo
parser.parse(data)