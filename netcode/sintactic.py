import ply.yacc as yacc
from lexer import listtokens
from lexer import data
import os
import webbrowser
import time

# Crear el parser
#parser = yacc.yacc()
# Analizar los datos de ejemplo
#parser.parse(data)

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
namelisttokens = 'fibonacci_recursivo12121.txt'

write_tokens_in_txt(listtokens, namelisttokens)

#print("-----------------------------------------------------------------------------")

def open_page_with_wait(url, segundos):
    print(f"Esperando {segundos} segundos antes de abrir la página...")
    time.sleep(segundos)
    webbrowser.open(url)

def seleccionar_pagina():
    print("¿Desea ingresar a una página para probar los tokens?")
    print("1. Parser Generator")
    print("2. JS Machines")
    print("3. Ninguna")
    opcion = input("Elija una opción (1, 2 o 3): ")
    if opcion == '1':
        url = "https://www.cs.princeton.edu/courses/archive/spring20/cos320/LL1/"
        print("Copie la gramatica grammar_ll1_parser y peguela en la web")
        open_page_with_wait(url, 3)
    elif opcion == '2':
        url = "https://jsmachines.sourceforge.net/machines/ll1.html"
        print("Copie la gramatica grammar_js_machine y peguela en la web")
        open_page_with_wait(url, 3)
    elif opcion == '3':
        print("Listo.")
    else:
        print("Opción no válida. Por favor, elija 1, 2 o 3.")

seleccionar_pagina()

#print("-----------------------------------------------------------------------------")