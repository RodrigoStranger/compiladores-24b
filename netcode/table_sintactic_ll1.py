import os
from lexic import tokens
import csv

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
    # Initialize FOLLOW sets only for non-terminals
    follow = {symbol: set() for symbol in gramatica.keys()}
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
                    elif symbol in gramatica:  # Non-terminal
                        if not follow[symbol].issuperset(trailer):
                            follow[symbol].update(trailer)
                            changed = True
                        if 'e' in first[symbol]:
                            trailer.update(first[symbol] - {'e'})
                        else:
                            trailer = first[symbol]
                    else:  # Terminal
                        trailer = first[symbol]  # FIRST of terminal is the terminal itself
    return follow

def construir_tabla_LL1(gramatica, first, follow, tokens):
    tabla = {}
    for no_terminal in gramatica:
        tabla[no_terminal] = {}
        for produccion in gramatica[no_terminal]:
            first_alpha = set()
            if produccion == ['e']:
                first_alpha.add('e')
            else:
                # Compute FIRST of the production
                for simbolo in produccion:
                    first_alpha.update(first[simbolo] - {'e'})
                    if 'e' not in first[simbolo]:
                        break
                else:
                    first_alpha.add('e')

            # For each terminal in FIRST(alpha)
            for terminal in first_alpha - {'e'}:
                tabla[no_terminal][terminal] = ' '.join(produccion)

            # If epsilon is in FIRST(alpha), add the production to FOLLOW(non_terminal)
            if 'e' in first_alpha:
                for terminal in follow[no_terminal]:
                    tabla[no_terminal][terminal] = ' '.join(produccion)
    return tabla

def escribir_tabla_csv(tabla, tokens, output_file):
    # Ensure all tokens are included, and include the end-of-input marker '$'
    all_terminals = tokens + ['$']

    # Prepare the header row with terminals
    header = [''] + all_terminals
    non_terminals = list(tabla.keys())

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)

        for non_terminal in non_terminals:
            row = [non_terminal]
            for terminal in all_terminals:
                entry = tabla[non_terminal].get(terminal, '')
                if entry:
                    entry = f"{non_terminal} -> {entry}"
                row.append(entry)
            writer.writerow(row)


# Import tokens from lexic module
from lexic import tokens  # Assuming tokens is correctly defined

# Read the grammar from the file
directory2 = os.path.dirname(__file__)
sketchfile = 'grammar.txt'
pathfile2 = os.path.join(directory2, '..', 'grammar', sketchfile)

gramatica_netcode = read_grammar(pathfile2)
conjunto_first = calcular_first_gramatica(gramatica_netcode, tokens)

# Assuming the start symbol is the first non-terminal in the grammar
start_symbol = next(iter(gramatica_netcode))

conjunto_follow = calcular_follow_gramatica(gramatica_netcode, conjunto_first, tokens, start_symbol)

# Display the FIRST sets
print("FIRST sets:")
for simbolo, first_set in conjunto_first.items():
    print(f"First({simbolo}) = {first_set}")

# Display the FOLLOW sets
print("\nFOLLOW sets:")
for simbolo, follow_set in conjunto_follow.items():
    print(f"Follow({simbolo}) = {follow_set}")

tabla_LL1 = construir_tabla_LL1(gramatica_netcode, conjunto_first, conjunto_follow, tokens)

# Output the parsing table to CSV
output_csv_file = 'parsing_table.csv'
escribir_tabla_csv(tabla_LL1, tokens, output_csv_file)

print(f"Parsing table has been written to {output_csv_file}")