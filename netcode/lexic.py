import os
import ply.lex as lex

from functions_lexic import *

directory = os.path.dirname(__file__)
sketchfile = 'types.txt'
pathfile = os.path.join(directory, '..', 'sketch', sketchfile)

tokens = ['FUNCION', 'ID', 'CORCHETEABI', 'CORCHETECERR', 'LLAVEABI', 'LLAVECERR', 'PROGRAMA', 'PRINCIPAL', 'TIPOENTERO', 'TIPOVACIO', 
             'VARIABLE', 'COMA', 'SI', 'SINO', 'ENTONCES', 'MIENTRAS', 'PARA', 'PUNTOYCOMA', 'IGUAL', 'DETENER', 'RETORNAR', 'IMPRIMIR', 
             'CONCATENAR', 'SUMA', 'RESTA', 'MULTIPLICACION', 'DIVISION', 'RESIDUO', 'IGUALBOOLEANO', 'MENORQUE', 'MAYORQUE', 'MENORIGUALQUE', 
             'MAYORIGUALQUE', 'DIFERENTEDE', 'Y', 'O', 'NCADENA', 'NDECIMAL', 'NENTERO', 'NBOOLEANO', 'TIPOCADENA', 'TIPODECIMAL', 'TIPOBOOLEANO', 
             'AUMENTAR', 'DISMINUIR']

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
t_CONCATENAR = r'\$'
t_COMA = r','

t_ignore = ' \t'

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

def t_error(t):
    print("Caracter Ilegal %s " % t.value[0])
    t.lexer.skip(1)
    
lexer = lex.lex()
lexer.input(generate_data(pathfile))
listtokens = []

print("Nombre del código puesto a revisión: ", sketchfile)
print(" ")

def generate_tokens(list_tokens):
    while True:
        tok = lexer.token()
        if not tok: break
        token_obj = Token(tok.type, tok.value, tok.lineno, tok.lexpos)
        list_tokens.append(token_obj)
    #print("Tokens generados correctamente.\n")
    print("Análisis léxico exitoso, tokens generados correctamente.\n")

generate_tokens(listtokens)
listtokens.append(Token("$", "$", None, None))

#print_tokens(listtokens)
#cambiar nombre cuando se quiere sacar tokens de cada codigo
#namelisttokens = 'prueba.txt'
#write_tokens_in_txt(listtokens, namelisttokens)