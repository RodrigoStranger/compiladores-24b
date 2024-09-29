from lexer import listtokens
from lexer import Token
from lexer import print_tokens
import pandas as pd
import os

directory2 = os.path.dirname(__file__)
sketchfile = 'table_ll1_example.csv'
pathfile2 = os.path.join(directory2, '..', 'table_ll1', sketchfile)

df = pd.read_csv(pathfile2, index_col = 0)
df = df.fillna('null')
print("Tabla ll1:")
print(df)

listtokens_example = []
def generate_token_example(type, listtokens):
    token_obj = Token(type, None, 0, 0)
    listtokens.append(token_obj)

# ejemplo: ( int )
generate_token_example("(", listtokens_example)
generate_token_example("int", listtokens_example)
generate_token_example(")", listtokens_example)

print_tokens(listtokens_example)