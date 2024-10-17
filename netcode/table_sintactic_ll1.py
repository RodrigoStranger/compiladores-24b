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
        first[token] = {token}
    return first

def calcular_first(simbolo, gramatica, first, visitados):
    if simbolo in first and first[simbolo]:
        return first[simbolo]

    if simbolo in visitados:
        return set()

    visitados.add(simbolo)
    first[simbolo] = set()

    for produccion in gramatica.get(simbolo, []):
        if produccion == ['e']:
            first[simbolo].add('e')
        else:
            for simbolo_produccion in produccion:
                simbolo_first = calcular_first(simbolo_produccion, gramatica, first, visitados)
                first[simbolo].update(simbolo_first - {'e'})
                if 'e' not in simbolo_first:
                    break
            else:
                first[simbolo].add('e')

    visitados.remove(simbolo)
    return first[simbolo]

def calcular_first_gramatica(gramatica, tokens):
    first = inicializar_first_terminales(tokens)
    for no_terminal in gramatica:
        calcular_first(no_terminal, gramatica, first, set())
    return first

def calcular_follow_gramatica(gramatica, first, tokens, start_symbol):
    # Initialize FOLLOW sets for both non-terminals and terminals
    symbols = list(gramatica.keys()) + tokens
    follow = {symbol: set() for symbol in symbols}

    # Add end-of-input marker to FOLLOW of start symbol
    follow[start_symbol].add('$')

    changed = True
    while changed:
        changed = False
        for lhs in gramatica:
            for production in gramatica[lhs]:
                trailer = follow[lhs].copy()
                for symbol in reversed(production):
                    if symbol == 'e':
                        continue  # Skip epsilon symbol
                    if symbol in gramatica:  # Non-terminal
                        if not follow[symbol].issuperset(trailer):
                            before_update = follow[symbol].copy()
                            follow[symbol].update(trailer)
                            if follow[symbol] != before_update:
                                changed = True
                        if 'e' in first[symbol]:
                            trailer.update(first[symbol] - {'e'})
                        else:
                            trailer = first[symbol]
                    else:  # Terminal
                        if not follow[symbol].issuperset(trailer):
                            before_update = follow[symbol].copy()
                            follow[symbol].update(trailer)
                            if follow[symbol] != before_update:
                                changed = True
                        trailer = first[symbol]  # For terminals, FIRST is the symbol itself
    return follow

# Example tokens (terminals)
tokens_example = ['id', '+', '*']
# Read the grammar from the file
directory2 = os.path.dirname(__file__)
sketchfile = 'grammar_example.txt'
pathfile2 = os.path.join(directory2, '..', 'grammar', sketchfile)

gramatica_netcode = read_grammar(pathfile2)
conjunto_first = calcular_first_gramatica(gramatica_netcode, tokens_example)

# Assuming the start symbol is the first non-terminal in the grammar
start_symbol = next(iter(gramatica_netcode))

conjunto_follow = calcular_follow_gramatica(gramatica_netcode, conjunto_first, tokens_example, start_symbol)

# Display the FIRST sets
print("FIRST sets:")
for simbolo, first_set in conjunto_first.items():
    print(f"First({simbolo}) = {first_set}")

# Display the FOLLOW sets
print("\nFOLLOW sets:")
for simbolo, follow_set in conjunto_follow.items():
    print(f"Follow({simbolo}) = {follow_set}")
