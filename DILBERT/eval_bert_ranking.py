import os
from argparse import ArgumentParser
import pickle
from copy import deepcopy
from typing import List, Dict, Any

import numpy as np
from tqdm import tqdm
import pandas as pd

from DILBERT.DILBERT.data_utils.utils import read_dataset, read_clinical_trials_dataset
from DILBERT.DILBERT.models.bert_ranker import RankingMapper


Entity = Dict[str, Any]


def check_label(predicted_cui: str, golden_cui: str) -> int:
    """
    Comparing composite concept_ids
    """
    return len(set(predicted_cui.replace('+', '|').split("|")).
               intersection(set(golden_cui.replace('+', '|').split("|")))) > 0


def is_correct(meddra_code: str, candidates: List[str], topk: int = 1) -> int:
    for candidate in candidates[:topk]:
        if check_label(candidate, meddra_code): return 1
    return 0


def create_parser():
    parser = ArgumentParser()
    parser.add_argument('--model_dir')
    parser.add_argument('--data_folder')
    parser.add_argument('--vocab')
    parser.add_argument('--split', action='store_true')
    parser.add_argument('--prediction', action='store_true')
    parser.add_argument('--ct_dataset', action='store_true')
    parser.add_argument('--out_of_kb', action='store_true')
    parser.add_argument('--output_path')

    return parser

#ask the authors on github about problem
#link part1 and dilbert together
#link dilbert and part2 together 
#run the generation pipeline

def eval_splitted_entities(predicted_entities: List[Entity], gold_entities: List[Entity]) -> float:
    gold_entities = pd.DataFrame(gold_entities)
    correct_top1 = []
    for pred_entity in predicted_entities:
        entity_id = pred_entity['entity_id'].split('_')[0]
        labels = gold_entities[gold_entities.entity_id == entity_id]['label'].iloc[0].split(',')
        for label in labels:
            is_pred_correct = is_correct(label, pred_entity['label'], topk=1)
            if is_pred_correct:
                correct_top1.append({'entity_id': entity_id, 'is_corr': is_pred_correct})
                break
    correct_top1 = pd.DataFrame(correct_top1)
    return correct_top1.groupby('entity_id')['is_corr'].agg('min').mean()


def eval_entities(predicted_entities: List[Entity], gold_entities: List[Entity]) -> float:
    correct_top1 = []
    for gold_entity, pred_entity in tqdm(zip(gold_entities, predicted_entities), total=len(gold_entities)):
        predicted_top_labels = pred_entity['label']
        label = gold_entity['label']
        correct_top1.append(is_correct(label, predicted_top_labels, topk=1))
    return np.mean(correct_top1)

def save_predictions(args, predicted):

    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path, exist_ok = True)

    with open(os.path.join(args.output_path, "NormPreds.tsv"), 'w') as df:
        df.write('id\tabstract_id\toffset_start\toffset_finish\ttype\tmention\tentity_ids\n')
        for i, entry in enumerate(predicted):
            fileName = '_'.join(entry['query_id'].split('_')[:-1])
            if i==0:
                with open(fileName, 'r') as f:
                    data = f.readlines()
            else:
                if(fileName != '_'.join(predicted[i-1]['query_id'].split('_')[:-1])):
                    with open(fileName, 'r') as f:
                        data = f.readlines()
            line = data[entry['entity_id']].split('||')
            base_name = os.path.basename(fileName.split('.')[0])
            offsets = line[1].split('|')
            df.write(f'{i}\t{base_name}\t{offsets[0]}\t{offsets[1]}\t{line[2]}\t{line[3]}\t{entry["label"][0]}\n')
        
def main(args):
    if args.ct_dataset:
        entities = read_clinical_trials_dataset(args.data_folder, args.out_of_kb)
    else:
        entities = read_dataset(args.data_folder)
        bert_ranker = RankingMapper(args.model_dir, args.vocab)
        predicted = bert_ranker.predict(entities)
        pickle.dump(predicted, open( "predicted.p", "wb" ))
        if not args.prediction:
            if args.split:
                acc_1 = eval_splitted_entities(predicted, entities)
            else:
                acc_1 = eval_entities(predicted, entities)
            print(f"Acc@1 is {acc_1}")
        else:
            save_predictions(args, predicted)

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    main(args)

