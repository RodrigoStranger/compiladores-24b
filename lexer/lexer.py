import ply.lex as lex

# Tokens de NetCode
tokens = ('FUNCION', 'PRINCIPAL', 'CORCHETEABI', 'CORCHETECERR', 'IMPRIMIR', 'COMILLAS', 'ID', 'FINALSENTENCIA', 
          'RETORNAR', 'DETENER', 'LLAVEABI', 'LLAVECERR', 'TIPOENTERO', 'TIPOCADENA', 'TIPODECIMAL', 'TIPOBOOLEANO', 
          'TIPOVACIO', 'SI', 'Y', 'O', 'NO', 'SINO', 'ENTONCES', 'MIENTRAS', 'PARA', 'SUMA', 'RESTA', 'MULTIPLICACION', 
          'DIVISION', 'RESIDUO', 'MENORQUE', 'MAYORQUE', 'MENORIGUALQUE', 'MAYORIGUALQUE', 'IGUAL', 'IGUALBOOLEANO', 'DIFERENTEDE', 
          'AUMENTAR', 'DISMINUIR', 'SUMAIGUAL', 'RESTAIGUAL', 'MULTIPLICACIONIGUAL', 'DIVISIONIGUAL', 'CONCATENAR', 'NENTERO', 'NDECIMAL', 
          'NCADENA', 'NBOOLEANO', 'COMENTARIO')

# Expresiones regulares para los tokens
t_FUNCION = r'function'
t_PRINCIPAL = r'main'
t_CORCHETEABI = r'\['
t_CORCHETECERR = r'\]'
t_IMPRIMIR = r'log'
t_COMILLAS = r'\"'
t_FINALSENTENCIA = r';'
t_RETORNAR = r'echo'
t_DETENER = r'stop'
t_LLAVEABI = r'\{'
t_LLAVECERR = r'\}'
t_TIPOENTERO = r'integer'
t_TIPOCADENA = r'text'
t_TIPODECIMAL = r'decimal'
t_TIPOBOOLEANO = r'boolean'
t_TIPOVACIO = r'void'
t_SI = r'if'
t_Y = r'and'
t_O = r'or'
t_NO = r'not'
t_SINO = r'elif'
t_ENTONCES = r'else'
t_MIENTRAS = r'while'
t_PARA = r'for'
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
t_NENTERO = r'-?\d+'
t_NDECIMAL = r'-?\d+\.\d+'
t_NCADENA = r'\"[^\"\n]*\"'
t_NBOOLEANO = r'(true|false)'
t_COMENTARIO = r'//.*'
t_ignore = ' \t'


# Palabras reservadas de NetCode
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
    'not': 'NO',
    'elif': 'SINO',
    'else': 'ENTONCES',
    'while': 'MIENTRAS',
    'for': 'PARA',
    'true': 'NBOOLEANO',
    'false': 'NBOOLEANO'
}

print(reserved)
print(tokens)