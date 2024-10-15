import os
from lexic import tokens

def read_grammar(ruta_archivo):
    gramatica = {}
    with open(ruta_archivo, 'r') as archivo:
        for linea in archivo:
            if linea.strip():
                lado_izquierdo, lado_derecho = linea.split('->')
                lado_izquierdo = lado_izquierdo.strip()
                producciones = [p.strip().split() for p in lado_derecho.split('|')]
                if lado_izquierdo in gramatica:
                    gramatica[lado_izquierdo].extend(producciones)
                else:
                    gramatica[lado_izquierdo] = producciones
    return gramatica

def inicializar_first_terminales(tokens):
    first = {}
    for token in tokens:
        first[token] = {token}  # El conjunto First del terminal es él mismo
    return first

def calcular_first(simbolo, gramatica, first):
    # Si el símbolo es un terminal (o epsilon), regresamos el mismo símbolo
    if simbolo in first:
        return first[simbolo]

    first[simbolo] = set()

    # Recorremos cada producción del símbolo
    for produccion in gramatica[simbolo]:
        if produccion == ['e']:  # Si la producción es epsilon
            first[simbolo].add('e')
        else:
            for simbolo_produccion in produccion:
                simbolo_first = calcular_first(simbolo_produccion, gramatica, first)
                first[simbolo].update(simbolo_first - {'e'})  # Añadir primeros excepto epsilon
                # Si el símbolo no genera epsilon, paramos
                if 'e' not in simbolo_first:
                    break
            else:
                # Si todos los símbolos de la producción generan epsilon, añadimos epsilon
                first[simbolo].add('e')
    return first[simbolo]

def calcular_first_gramatica(gramatica, tokens):
    first = inicializar_first_terminales(tokens)  # Inicializar First para los terminales
    for no_terminal in gramatica:
        calcular_first(no_terminal, gramatica, first)
    return first

# Ejemplo de uso
tokens_example = ['int', ')', '(', '+', '*']
# Cálculo del conjunto First para la gramática
directory2 = os.path.dirname(__file__)
sketchfile = 'grammar.txt'
pathfile2 = os.path.join(directory2, '..', 'grammar', sketchfile)

gramatica_netcode = read_grammar(pathfile2)
conjunto_first = calcular_first_gramatica(gramatica_netcode, tokens)

# Mostrar los conjuntos First para cada símbolo (terminales y no terminales)
for simbolo, first_set in conjunto_first.items():
    print(f"First({simbolo}) = {first_set}")