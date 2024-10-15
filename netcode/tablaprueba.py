import os
from lexic import tokens
import csv

def read_grammar(ruta_archivo):
    gramatica = {}
    with open(ruta_archivo, 'r') as archivo:
        for linea in archivo:
            # Ignorar líneas vacías
            if linea.strip():
                # Separar la parte izquierda y derecha de la producción
                lado_izquierdo, lado_derecho = linea.split('->')
                lado_izquierdo = lado_izquierdo.strip()
                
                # Separar las producciones por el símbolo |
                producciones = [p.strip().split() for p in lado_derecho.split('|')]
                
                # Añadir la producción al diccionario
                if lado_izquierdo in gramatica:
                    gramatica[lado_izquierdo].extend(producciones)
                else:
                    gramatica[lado_izquierdo] = producciones
                    
    return gramatica


directory2 = os.path.dirname(__file__)
sketchfile = 'grammar_example.txt'
pathfile2 = os.path.join(directory2, '..', 'grammar', sketchfile)

gramatica_netcode = read_grammar(pathfile2)
print(gramatica_netcode)
# Función para inicializar First para los terminales
def inicializar_first_terminales(tokens):
    first = {}
    for token in tokens:
        first[token] = {token}  # El conjunto First del terminal es él mismo
    return first

# Función para calcular el conjunto First de un símbolo
def calcular_first(simbolo, gramatica, first):
    # Si el símbolo es un terminal (o epsilon), regresamos el mismo símbolo
    if simbolo in tokens or simbolo == 'e':  # Aquí se maneja 'e' como epsilon
        return {simbolo}

    # Si el símbolo ya tiene su conjunto First calculado, lo regresamos
    if simbolo in first:
        return first[simbolo]

    # Inicializamos el conjunto First para el símbolo
    first[simbolo] = set()

    # Recorremos cada producción del símbolo
    for produccion in gramatica[simbolo]:
        # Si la producción es vacía (epsilon), lo agregamos al conjunto First
        if produccion == ['e']:  # Si la producción es epsilon
            first[simbolo].add('e')
        else:
            # Recorremos los símbolos de la producción
            for simbolo_produccion in produccion:
                simbolo_first = calcular_first(simbolo_produccion, gramatica, first)

                # Añadir los primeros del símbolo de la producción al conjunto First
                first[simbolo].update(simbolo_first - {'e'})

                # Si el símbolo no genera epsilon, paramos
                if 'e' not in simbolo_first:
                    break
            else:
                # Si todos los símbolos de la producción generan epsilon, añadimos epsilon
                first[simbolo].add('e')

    return first[simbolo]


# Función para calcular el conjunto First para toda la gramática
def calcular_first_gramatica(gramatica, tokens):
    first = inicializar_first_terminales(tokens)  # Inicializar First para los terminales
    for no_terminal in gramatica:
        calcular_first(no_terminal, gramatica, first)
    return first


tokens_example = ['int', ')', '(', '+', '*']
# Cálculo del conjunto First para la gramática
conjunto_first = calcular_first_gramatica(gramatica_netcode, tokens_example)

# Mostrar los conjuntos First para cada símbolo (terminales y no terminales)
for simbolo, first_set in conjunto_first.items():
    print(f"First({simbolo}) = {first_set}")

