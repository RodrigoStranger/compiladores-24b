import os
from functions import generate_data
from lexer import tokens
import csv

# Cargar la gramática desde un archivo
directory = os.path.dirname(__file__)
sketchfile = 'grammar_js_machines.txt'
pathfile = os.path.join(directory, '..', 'grammar', sketchfile)

# Generar datos (presumiblemente devuelve una ruta de archivo)
grammar = generate_data(pathfile)

class Grammar:
    def __init__(self):
        self.EPSILON = ''
        self.alphabet = []
        self.nonterminals = []
        self.terminals = []
        self.rules = {}
        self.firsts = {}
        self.follows = {}
        self.rule_table = {}

    def add_rule(self, lhs, rhs):
        if lhs not in self.rules:
            self.rules[lhs] = []
        self.rules[lhs].append(rhs)

    def collect_alphabet_nonterminals_terminals(self):
        for lhs in self.rules:
            self.nonterminals.append(lhs)
            for rhs in self.rules[lhs]:
                for symbol in rhs:
                    if symbol not in self.nonterminals and symbol not in self.terminals and symbol != self.EPSILON:
                        self.terminals.append(symbol)
        
        self.alphabet = self.nonterminals + self.terminals

    def calculate_first(self):
        for nt in self.nonterminals:
            self.firsts[nt] = self.first(nt)

    def first(self, symbol):
        if symbol in self.terminals:
            return {symbol}
        if symbol == self.EPSILON:
            return {self.EPSILON}
        
        first_set = set()
        for production in self.rules.get(symbol, []):
            for sym in production:
                first_of_sym = self.first(sym)
                first_set.update(first_of_sym)
                if self.EPSILON not in first_of_sym:
                    break
            else:
                first_set.add(self.EPSILON)
        return first_set

    def calculate_follow(self):
        for nt in self.nonterminals:
            self.follows[nt] = set()
        self.follows[self.nonterminals[0]].add('$')  # Asumimos que el primer no terminal es el símbolo de inicio
        
        while True:
            updated = False
            for nt in self.nonterminals:
                for lhs in self.rules:
                    for production in self.rules[lhs]:
                        if nt in production:
                            idx = production.index(nt)
                            if idx + 1 < len(production):
                                next_symbol = production[idx + 1]
                                first_of_next = self.first(next_symbol)
                                if self.EPSILON in first_of_next:
                                    first_of_next.remove(self.EPSILON)
                                    self.follows[nt].update(first_of_next)
                                    self.follows[nt].update(self.follows[lhs])
                                else:
                                    self.follows[nt].update(first_of_next)
                            else:
                                self.follows[nt].update(self.follows[lhs])
            if not updated:
                break

    def make_rule_table(self):
        for lhs in self.rules:
            for rhs in self.rules[lhs]:
                first_set = self.first(rhs[0]) if rhs else set()
                for terminal in first_set:
                    if terminal != self.EPSILON:
                        if lhs not in self.rule_table:
                            self.rule_table[lhs] = {}
                        self.rule_table[lhs][terminal] = rhs
                if self.EPSILON in first_set:
                    for terminal in self.follows[lhs]:
                        if lhs not in self.rule_table:
                            self.rule_table[lhs] = {}
                        self.rule_table[lhs][terminal] = rhs

    def save_to_csv(self, filename):
        with open(filename, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            headers = ["Nonterminal"] + sorted(self.terminals)
            writer.writerow(headers)

            for nt in sorted(self.rule_table.keys()):
                row = [nt]
                for terminal in sorted(self.terminals):
                    if terminal in self.rule_table[nt]:
                        row.append(" | ".join(self.rule_table[nt][terminal]))
                    else:
                        row.append("")
                writer.writerow(row)


def load_grammar_from_file(filename):
    grammar = Grammar()
    with open(filename, 'r') as file:
        current_lhs = None
        for line in file:
            line = line.strip()
            if '->' in line:
                current_lhs, rhs = line.split('->')
                current_lhs = current_lhs.strip()
                rhs = rhs.strip().split()  # Separar los símbolos de la producción
                grammar.add_rule(current_lhs, rhs)
            elif line:  # Si hay más producciones para el mismo LHS
                rhs = line.strip().split()  # Separar los símbolos de la producción
                grammar.add_rule(current_lhs, rhs)
    return grammar


output_folder = 'table_ll1'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
output_csv_path = os.path.join(output_folder, 'table_ll1.csv')

# Cargar la gramática desde el archivo
grammar = load_grammar_from_file(pathfile)
grammar.collect_alphabet_nonterminals_terminals()
grammar.calculate_first()
grammar.calculate_follow()
grammar.make_rule_table()
grammar.save_to_csv(output_csv_path)  # Cambié la variable aquí

print(f"Tabla LL(1) guardada en {output_csv_path}.")
