import ply.yacc as yacc
from lexer import tokens
from lexer import lex
from lexer import data

# Define la gramática aquí
def p_program(p):
    '''program : statements'''
    print("Programa analizado correctamente")

def p_statements(p):
    '''statements : statements statement
                  | statement'''
    pass

def p_statement(p):
    '''statement : FUNCION ID LLAVEABI statements LLAVECERR FINALSENTENCIA
                 | PRINCIPAL LLAVEABI statements LLAVECERR FINALSENTENCIA
                 | IMPRIMIR ID FINALSENTENCIA
                 | RETORNAR ID FINALSENTENCIA
                 | DETENER FINALSENTENCIA'''
    pass

def p_error(p):
    if p:
        print(f"Error de sintaxis en el token '{p.type}'")
    else:
        print("Error de sintaxis en el final de archivo")

# Crear el parser
parser = yacc.yacc()


# Analizar los datos de ejemplo
parser.parse(data)