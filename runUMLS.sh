#!/bin/bash
DATA_DIR=./data/LITCOINDILBERTPREPARED/
TRIPLETS_FOLDER=./data/corpora/litcoin/
TRIPLETS_FILE=train_neg30_pos30_parents2_random.txt
BERT_MODEL=./data/pretrained_models/biobert-base-cased-v1.2
OUTPUT_DIR=./tmp/litcoin



PREPARE_TRIPLETS=true
TRAIN_MODEL=true
EVAL_MODEL=true


if $PREPARE_TRIPLETS; then
  mkdir -p $TRIPLETS_FOLDER
  PYTHONPATH=$(pwd) python data_utils/convert_to_triplet_dataset.py --input_data $DATA_DIR/train \
                                       --vocab $DATA_DIR/MSHOMIMVocab.txt \
                                       --hierarchy_aware \
                                       --hierarchy $DATA_DIR/UMLSgraph.csv \
                                       --UMLS \
                                       --save_to $TRIPLETS_FOLDER/$TRIPLETS_FILE
fi

if $TRAIN_MODEL; then
  mkdir -p $OUTPUT_DIR
  PYTHONPATH=$(pwd) python train_sentence_bert.py --path_to_bert_model $BERT_MODEL \
                                --data_folder $TRIPLETS_FOLDER \
                                --triplets_file $TRIPLETS_FILE \
                                --output_dir $OUTPUT_DIR
fi

if $EVAL_MODEL; then
  PYTHONPATH=$(pwd) python eval_bert_ranking.py --model_dir $OUTPUT_DIR \
                            --data_folder $DATA_DIR/test \
                            --vocab $DATA_DIR/MSHOMIMVocab.txt  > $DATA_DIR/eval_results.txt
fi
