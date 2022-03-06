DATA_DIR=./data/coling_datasets/bc5cdr-disease/
TRIPLETS_FOLDER=./data/corpora/labelling/triplets/
TRIPLETS_FILE=train_neg30_pos30_parents2_random.txt
BERT_MODEL=./data/pretrained_models/biobert-v1.1
OUTPUT_DIR=./tmp/test_run
PYTHONPATH=$(dirname $(pwd))


PREPARE_TRIPLETS=false
TRAIN_MODEL=true
EVAL_MODEL=true


if $PREPARE_TRIPLETS; then
  #mkdir $TRIPLETS_FOLDER
  PYTHONPATH=/home/ksasse/code/alzheimers/DILBERT python data_utils/convert_to_triplet_dataset.py --input_data $DATA_DIR/processed_traindev \
                                       --vocab $DATA_DIR/train_dictionary.txt \
                                       --save_to $TRIPLETS_FOLDER/$TRIPLETS_FILE
fi

if $TRAIN_MODEL; then
  PYTHONPATH=/home/ksasse/code/alzheimers/DILBERT python train_sentence_bert.py --path_to_bert_model $BERT_MODEL \
                                --data_folder $TRIPLETS_FOLDER \
                                --triplets_file $TRIPLETS_FILE \
                                --output_dir $OUTPUT_DIR
fi

if $EVAL_MODEL; then
  PYTHONPATH=/home/ksasse/code/litcoinsasse/DILBERT python eval_bert_ranking.py --model_dir $OUTPUT_DIR \
                            --data_folder $DATA_DIR/processed_test_refined \
                            --vocab $DATA_DIR/test_dictionary.txt > $DATA_DIR/eval_results.txt
fi
