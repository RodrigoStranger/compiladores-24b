import os

#class Token
class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

#funcion que genera una data a partir de un boceto de lenguaje
def generate_data(name_pathfile):
    try:
        with open(name_pathfile, 'r') as file:
            data = file.read()
    except FileNotFoundError:
        print(f"Error: El archivo '{name_pathfile}' no se encontró.")
        data = ''
    return data

#funcion que imprime tokens
def print_tokens(list_tokens):
    print("Tokens NetCode: ")
    for token in list_tokens:
        print(token.type, token.value)
        #print(token.type)

#funcion que escribe tokens en un txt
def write_tokens_in_txt(lista_tokens, nombre_archivo):
    carpeta_salida = 'listtokens'
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
    archivo_salida = os.path.join(carpeta_salida, nombre_archivo)
    try:
        with open(archivo_salida, 'w') as file:
            tokens = ' '.join([token.type for token in lista_tokens])
            file.write(tokens)
            print(f"Tokens escritos exitosamente en el archivo '{archivo_salida}'.\n")
    except Exception as e:
        print(f"Error al escribir los tokens en el archivo: {str(e)}")