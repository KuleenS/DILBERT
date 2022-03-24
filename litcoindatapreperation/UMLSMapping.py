# %%
import mysql.connector
import pandas as pd

# %%
query = ("SELECT DISTINCT MRREL.AUI2, MRREL.AUI1, MRREL.REL, SAB FROM MRREL WHERE (REL = 'PAR' or REL='CHD') and (SAB LIKE '%MSH%' OR SAB LIKE '%OMIM%')")

conn = mysql.connector.connect(user='', password='', database='', host='')
cursor = conn.cursor()

# %%
cursor.execute(query)

# %%
total_relations_umls = []
for x in cursor:
    total_relations_umls.append(x)

# %%
df = pd.DataFrame(total_relations_umls, columns =['FirstAUI', 'SecondAUI', 'REL','SAB'])

# %%
query2 = ("SELECT AUI, SAB, CODE, STR FROM MRCONSO WHERE (SAB LIKE '%MSH%' OR SAB LIKE '%OMIM%') and ISPREF = 'Y'")

# %%
cursor.execute(query2)

# %%
names_of_CUIS = []
for x in cursor:
    names_of_CUIS.append(x)

# %%
df2 = pd.DataFrame(names_of_CUIS, columns =['AUI', 'SAB', 'CODE','STR'])

# %%
result = df.merge(df2, left_on="FirstAUI", right_on="AUI")

# %%
result = result.drop(['SAB_x','SAB_y', 'AUI'], axis=1)

# %%
result = result.merge(df2, left_on="SecondAUI", right_on="AUI")

# %%
result = result.drop(['AUI','SAB', 'AUI'], axis=1)

# %%
result.columns = ['FirstAUI', 'SecondAUI', 'REL', 'CODE_First', 'STR_First', 'CODE_Second','STR_Second']

# %%
result = result.groupby(['CODE_First','REL', 'STR_First'])['CODE_Second'].apply(list).reset_index()

# %%
import os
os.mkdir('../data/LITCOINDILBERTPREPARED')
result.to_csv('../data/LITCOINDILBERTPREPARED/UMLSgraph.csv')

# %%
with open('../data/LITCOINDILBERTPREPARED/MSHOMIMVocab.txt', 'w') as f:
    for i,v in df2.iterrows():
        f.write(f'{v["CODE"]}||{v["STR"]}\n')


