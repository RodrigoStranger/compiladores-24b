import os
import csv
from collections import defaultdict
from lexic import tokens

def read_grammar_from_file(filename):
    grammar = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            # Eliminar comentarios y espacios en blanco
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # Saltar líneas vacías y comentarios
            if '->' not in line:
                continue  # Saltar líneas no válidas
            lhs, rhs = line.split('->', 1)
            lhs = lhs.strip()
            rhs = rhs.strip()
            productions = rhs.split('|')
            grammar.setdefault(lhs, [])
            for production in productions:
                # Dividir la producción en símbolos
                symbols = production.strip().split()
                grammar[lhs].append(symbols)
    return grammar

directory = os.path.dirname(__file__)
sketchfile = 'grammar.txt'
pathfile = os.path.join(directory, '..', 'grammar', sketchfile)

grammar = read_grammar_from_file(pathfile)
#tokens = ['id', '+', '*']
tokens.append('$')
# Lista de símbolos no terminales
non_terminals = list(grammar.keys())

# Inicializar FIRST y FOLLOW
FIRST = defaultdict(set)
FOLLOW = defaultdict(set)

# Funciones para calcular FIRST y FOLLOW
def compute_first(symbol):
    if symbol in FIRST and FIRST[symbol]:
        return FIRST[symbol]
    if symbol in tokens:
        FIRST[symbol] = set([symbol])
        return FIRST[symbol]
    first = set()
    for production in grammar[symbol]:
        if production[0] == 'e':
            first.add('e')
        else:
            for sym in production:
                sym_first = compute_first(sym)
                first.update(sym_first - set(['e']))
                if 'e' not in sym_first:
                    break
            else:
                first.add('e')
    FIRST[symbol] = first
    return first

def compute_follow(symbol):
    if symbol == list(grammar.keys())[0]:  # FOLLOW del símbolo inicial
        FOLLOW[symbol].add('$')
    for lhs in grammar:
        for production in grammar[lhs]:
            for i, sym in enumerate(production):
                if sym == symbol:
                    if i + 1 < len(production):
                        next_sym = production[i + 1]
                        next_first = compute_first(next_sym)
                        FOLLOW[symbol].update(next_first - set(['e']))
                        if 'e' in next_first:
                            FOLLOW[symbol].update(FOLLOW[lhs])
                    else:
                        if lhs != symbol:
                            FOLLOW[symbol].update(FOLLOW[lhs])

# Calcular FIRST para todos los símbolos
for non_terminal in non_terminals:
    compute_first(non_terminal)

# Calcular FOLLOW para todos los símbolos
for non_terminal in non_terminals:
    FOLLOW[non_terminal] = set()

changed = True
while changed:
    changed = False
    for non_terminal in non_terminals:
        before = len(FOLLOW[non_terminal])
        compute_follow(non_terminal)
        after = len(FOLLOW[non_terminal])
        if before != after:
            changed = True

# Construir la tabla LL(1)
ll1_table = defaultdict(dict)

for lhs in grammar:
    for production in grammar[lhs]:
        firsts = set()
        if production[0] == 'e':
            firsts.add('e')
        else:
            for sym in production:
                sym_first = compute_first(sym)
                firsts.update(sym_first - set(['e']))
                if 'e' not in sym_first:
                    break
            else:
                firsts.add('e')

        for terminal in firsts - set(['e']):
            ll1_table[lhs][terminal] = ' '.join(production)
        if 'e' in firsts:
            for terminal in FOLLOW[lhs]:
                ll1_table[lhs][terminal] = 'e'

# Crear la tabla LL(1) en formato CSV
csv_filename = 'table_ll1_pariente.csv'
carpeta_salida = 'table_ll1'
if not os.path.exists(carpeta_salida):
    os.makedirs(carpeta_salida)
archivo_salida = os.path.join(carpeta_salida, csv_filename)

with open(archivo_salida, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Escribir encabezados
    headers = [''] + tokens
    csvwriter.writerow(headers)
    # Escribir filas de la tabla
    for idx, nt in enumerate(non_terminals):
        row = [nt]
        for t in tokens:
            action = ll1_table[nt].get(t, '')
            row.append(action)
        csvwriter.writerow(row)

# Reabrir el archivo en modo lectura/escritura y eliminar la última línea si está vacía
with open(archivo_salida, 'rb+') as csvfile:
    csvfile.seek(-2, os.SEEK_END)
    while csvfile.tell() > 0 and csvfile.read(1) in [b'\n', b'\r']:
        csvfile.seek(-2, os.SEEK_CUR)
    if csvfile.tell() > 0:
        csvfile.truncate()

print(f"Tabla LL(1) exportada a {archivo_salida}")