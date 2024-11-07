import os
import csv
from collections import defaultdict
from lexic import tokens

directory = os.path.dirname(__file__)
sketchfile = 'grammar_js_machines.txt'
pathfile = os.path.join(directory, '..', 'grammar', sketchfile)

def read_grammar_word_file(filename):
    grammar = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '->' in line:
                lhs, rhs = line.split('->', 1)
            elif '::=' in line:
                lhs, rhs = line.split('::=', 1)
            else:
                continue
            lhs = lhs.strip()
            rhs = rhs.strip()
            symbols = rhs.split()
            symbols = ['e' if symbol == "''" else symbol for symbol in symbols]
            if lhs not in grammar:
                grammar[lhs] = []
            grammar[lhs].append(symbols)
    return grammar

def read_grammar_comun_file(filename):
    grammar = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '->' not in line:
                continue
            lhs, rhs = line.split('->', 1)
            lhs = lhs.strip()
            rhs = rhs.strip()
            productions = rhs.split('|')
            grammar.setdefault(lhs, [])
            for production in productions:
                symbols = production.strip().split()
                grammar[lhs].append(symbols)
    return grammar

grammar = read_grammar_word_file(pathfile)
tokens.append('$')
non_terminals = list(grammar.keys())

FIRST = defaultdict(set)
FOLLOW = defaultdict(set)

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
    if symbol == list(grammar.keys())[0]:
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

for non_terminal in non_terminals:
    compute_first(non_terminal)

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

csv_filename = 'table_ll1_parent2.csv'
carpeta_salida = 'table_ll1'

if not os.path.exists(carpeta_salida):
    os.makedirs(carpeta_salida)

archivo_salida = os.path.join(carpeta_salida, csv_filename)

with open(archivo_salida, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    headers = [''] + tokens
    csvwriter.writerow(headers)
    for idx, nt in enumerate(non_terminals):
        row = [nt]
        for t in tokens:
            action = ll1_table[nt].get(t, '')
            row.append(action)
        csvwriter.writerow(row)

with open(archivo_salida, 'rb+') as csvfile:
    csvfile.seek(-2, os.SEEK_END)
    while csvfile.tell() > 0 and csvfile.read(1) in [b'\n', b'\r']:
        csvfile.seek(-2, os.SEEK_CUR)
    if csvfile.tell() > 0:
        csvfile.truncate()

print(f"Tabla LL(1) exportada a {archivo_salida}")