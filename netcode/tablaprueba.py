import os
from lexic import tokens
import csv

def read_grammar(archivo):
    gramatica = {}
    with open(archivo, 'r') as f:
        for linea in f:
            linea = linea.strip()  # Eliminar espacios en blanco al inicio y al final
            if not linea:  # Ignorar líneas vacías
                continue  # Saltar a la siguiente iteración del bucle
            partes = linea.split('->')
            if len(partes) != 2:
                raise ValueError(f"Línea mal formada: {linea}")
            no_terminal = partes[0].strip()
            producciones = [prod.strip() for prod in partes[1].split('|')]
            gramatica[no_terminal] = producciones
    return gramatica

directory2 = os.path.dirname(__file__)
sketchfile = 'grammar.txt'
pathfile2 = os.path.join(directory2, '..', 'grammar', sketchfile)

gramatica = read_grammar(pathfile2)
print(gramatica)
print(" ")
print(tokens)


