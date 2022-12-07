import pandas as pd
from typing import Dict
from tqdm import tqdm
import ast


#UMLS version of MESH Graph
class UMLSGraph:
    def __init__(self, umls_path: str) -> None:
        #reads CSV and makes tree
        self.umls = pd.read_csv(umls_path)
        self.tree = {}
        self.create_tree(self.umls)

    def create_tree(self, mesh: pd.DataFrame) -> Dict[str, Dict[str, str]]:
        #loops through CSV and gets the fills in the child and parents of each CUI
        for row_idx, UMLS_ENTRY in tqdm(enumerate(mesh.itertuples(index=False)), total=mesh.shape[0]):
            node = self.get_node(UMLS_ENTRY)
            if UMLS_ENTRY.REL=='CHD':
                node['parents'].extend(ast.literal_eval(UMLS_ENTRY.CODE_Second))
            if UMLS_ENTRY.REL=='PAR':
                node['children'].extend(ast.literal_eval(UMLS_ENTRY.CODE_Second))

    def get_node(self, row):
        #returns the node of the tree
        if row.CODE_First in self.tree:
            node = self.tree[row.CODE_First]
        else:
            node = {
                'concept_id': row.CODE_First,
                'concept_name': row.STR_First,
                'parents': [],
                'children': []
            }
            self.tree[row.CODE_First] = node
        return node

    def get_parents(self, concept_id: str):
        if concept_id not in self.tree: return []
        return self.tree[concept_id]['parents']

    def get_children(self, concept_id: str):
        if concept_id not in self.tree: return []
        return self.tree[concept_id]['children']
