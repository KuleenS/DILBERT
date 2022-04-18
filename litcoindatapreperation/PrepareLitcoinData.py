# %%
import pandas as pd

# %%

#load the train and test for training data 
entities_train = pd.read_csv('../data/LITCOIN/entities_train.csv', sep='\t')
entities_test = pd.read_csv('../data/LITCOIN/entities_test.csv', sep='\t')

# %%
import os
#create the DILBERT prepared folders
os.makedirs('../data/LITCOINDILBERTPREPARED/train/')
os.makedirs('../data/LITCOINDILBERTPREPARED/test/')

# %%

#get all the DiseaseOrPhenotypicFeature from entities train and put them into dilbert training data
for abstract_id in entities_train.abstract_id.unique():
    temp_df = entities_train[entities_train.abstract_id == abstract_id]
    with open(f'../data/LITCOINDILBERTPREPARED/train/{abstract_id}.concept', 'w') as f:
        for i,v in temp_df.iterrows():
            if v['type']=='DiseaseOrPhenotypicFeature':
                f.write(f"{abstract_id}||{v['offset_start']}|{v['offset_finish']}||{v['type']}||{v['mention']}||{v['entity_ids']}\n")


#get all the DiseaseOrPhenotypicFeature from entities train and put them into dilbert testing data
for abstract_id in entities_test.abstract_id.unique():
    temp_df = entities_test[entities_test.abstract_id == abstract_id]
    with open(f'../data/LITCOINDILBERTPREPARED/test/{abstract_id}.concept', 'w') as f:
        for i,v in temp_df.iterrows():
            if v['type']=='DiseaseOrPhenotypicFeature':
                f.write(f"{abstract_id}||{v['offset_start']}|{v['offset_finish']}||{v['type']}||{v['mention']}||{v['entity_ids']}\n")

# %%



