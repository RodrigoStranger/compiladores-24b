import os
import ply.lex as lex

directory = os.path.dirname(__file__)
sketchfile = 'hola_mundo.txt'
pathfile = os.path.join(directory, '..', 'sketch', sketchfile)

tokens = ('FUNCION', 'PRINCIPAL', 'CORCHETEABI', 'CORCHETECERR', 'IMPRIMIR', 'ID', 
          'RETORNAR', 'DETENER', 'LLAVEABI', 'LLAVECERR', 'TIPOENTERO', 'TIPOCADENA', 'TIPODECIMAL', 'TIPOBOOLEANO', 
          'TIPOVACIO', 'SI', 'Y', 'O', 'SINO', 'ENTONCES', 'MIENTRAS', 'PARA', 'SUMA', 'RESTA', 'MULTIPLICACION', 
          'DIVISION', 'RESIDUO', 'MENORQUE', 'MAYORQUE', 'MENORIGUALQUE', 'MAYORIGUALQUE', 'IGUAL', 'IGUALBOOLEANO', 'DIFERENTEDE', 
          'AUMENTAR', 'DISMINUIR', 'SUMAIGUAL', 'RESTAIGUAL', 'MULTIPLICACIONIGUAL', 'DIVISIONIGUAL', 'CONCATENAR', 'NENTERO', 'NDECIMAL', 
          'NCADENA', 'NBOOLEANO', 'COMENTARIO', 'COMA', 'VARIABLE', 'PUNTOYCOMA', 'PROGRAMA') 

reserved = {    
    'function': 'FUNCION',
    'main': 'PRINCIPAL',
    'log': 'IMPRIMIR',
    'echo': 'RETORNAR',
    'stop': 'DETENER',
    'interger': 'TIPOENTERO',
    'text': 'TIPOCADENA',
    'decimal': 'TIPODECIMAL',
    'boolean': 'TIPOBOOLEANO',
    'void': 'TIPOVACIO',
    'if': 'SI',
    'and': 'Y',
    'or': 'O',
    'elif': 'SINO',
    'else': 'ENTONCES',
    'while': 'MIENTRAS',
    'for': 'PARA',
    'true': 'NBOOLEANO',
    'false': 'NBOOLEANO',
    'var' : 'VARIABLE',
    'program' : 'PROGRAMA'
}

t_PUNTOYCOMA = r';'
t_CORCHETEABI = r'\['
t_CORCHETECERR = r'\]'
t_LLAVEABI = r'\{'
t_LLAVECERR = r'\}'
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_RESIDUO = r'%'
t_MENORQUE = r'<'
t_MAYORQUE = r'>'
t_MENORIGUALQUE = r'<='
t_MAYORIGUALQUE = r'>='
t_IGUAL = r'='
t_IGUALBOOLEANO = r'=='
t_DIFERENTEDE = r'!='
t_AUMENTAR = r'\+\+'
t_DISMINUIR = r'--'
t_SUMAIGUAL = r'\+='
t_RESTAIGUAL = r'-='
t_MULTIPLICACIONIGUAL = r'\*='
t_DIVISIONIGUAL = r'/='
t_CONCATENAR = r'\$'
t_COMA = r','

def t_NCADENA(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NDECIMAL(t):
    r'-?\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NENTERO(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

def t_COMENTARIO(t):
    r'//.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print("Caracter Ilegal %s " % t.value[0])
    t.lexer.skip(1)
    
lexer = lex.lex()

#data = ''''''

def generate_data(name_pathfile):
    try:
        with open(name_pathfile, 'r') as file:
            data = file.read()
    except FileNotFoundError:
        print(f"Error: El archivo '{name_pathfile}' no se encontró.")
        data = ''
    return data

lexer.input(generate_data(pathfile))

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

listtokens = []

def generate_tokens(list_tokens):
    while True:
        tok = lexer.token()
        if not tok: break
        token_obj = Token(tok.type, tok.value, tok.lineno, tok.lexpos)
        list_tokens.append(token_obj)
    print("Log: Tokens generados correctamente.\n")

def print_tokens(list_tokens):
    print("Tokens NetCode: ")
    for token in list_tokens:
    #print(token.type, token.value)
        print(token.type)

#generate_tokens(listtokens)

#print_tokens(listtokens)

'''
def write_tokens_in_txt(lista_tokens, nombre_archivo):
    carpeta_salida = 'listtokens'
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
    archivo_salida = os.path.join(carpeta_salida, nombre_archivo)
    try:
        with open(archivo_salida, 'w') as file:
            tokens = ' '.join([token.type for token in lista_tokens])
            file.write(tokens)
            print(f"Tokens escritos exitosamente en el archivo '{archivo_salida}'.")
    except Exception as e:
        print(f"Error al escribir los tokens en el archivo: {str(e)}")

# cambiar nombre cuando se quiere sacar tokens de cada codigo
namelisttokens = 'hola_mundo_tokens.txt'

write_tokens_in_txt(listtokens, namelisttokens)
'''