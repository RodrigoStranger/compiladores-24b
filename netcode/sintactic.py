# parser.py
import ply.yacc as yacc
import importlib.util
import sys

# Ruta al archivo lexer.py
file_path = 'C:/Users/rodrigo/Documents/compiladores-24b/lexer/lexer.py'

# Cargar el módulo
spec = importlib.util.spec_from_file_location("lexer", file_path)
lexer = importlib.util.module_from_spec(spec)
sys.modules["lexer"] = lexer
spec.loader.exec_module(lexer)

from lexer import tokens

# Reglas gramaticales
def p_program(p):
    '''program : statements'''
    p[0] = p[1]

def p_statements(p):
    '''statements : statements statement
                   | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement_expr(p):
    '''statement : expression FINALSENTENCIA'''
    p[0] = p[1]

def p_statement_function(p):
    '''statement : FUNCION ID CORCHETEABI params CORCHETECERR TIPOENTERO LLAVEABI statements LLAVECERR'''
    p[0] = ('function', p[2], p[4], p[7])

def p_params(p):
    '''params : params COMA param
              | param'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_param(p):
    '''param : ID TIPOENTERO
             | ID TIPODECIMAL
             | ID TIPOCADENA'''
    p[0] = (p[1], p[2])

def p_expression_binop(p):
    '''expression : expression SUMA expression
                  | expression RESTA expression'''
    p[0] = (p[2], p[1], p[3])

def p_expression_number(p):
    '''expression : NENTERO
                  | NDECIMAL'''
    p[0] = p[1]

def p_expression_id(p):
    '''expression : ID'''
    p[0] = p[1]

def p_error(p):
    print(f"Error de sintaxis en el token: {p.value if p else 'EOF'}")

# Crear el parser
parser = yacc.yacc()

# Función para analizar el código
def parse_code(data):
    return parser.parse(data)

# Código de ejemplo
if __name__ == "__main__":
    data = 'function suma[x integer, y integer] integer {echo x+y;}'
    parse_code(data)