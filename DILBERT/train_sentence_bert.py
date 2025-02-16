from argparse import ArgumentParser
from sentence_transformers.readers import TripletReader

from DILBERT.DILBERT.models.bert_ranker import RankingMapper

def create_parser():
    parser = ArgumentParser()
    parser.add_argument('--path_to_bert_model')
    parser.add_argument('--data_folder')
    parser.add_argument('--batch_size', type=int, default=64)
    parser.add_argument('--epochs', type=int, default=2)
    parser.add_argument('--triplets_file')
    parser.add_argument('--output_dir')
    return parser

def main(args):
    model = RankingMapper(model_path=args.path_to_bert_model)

    data_reader = TripletReader(args.data_folder)
    model.train(data_reader, args.batch_size, args.epochs, args.output_dir, args.triplets_file)

if __name__ == '__main__':

    parser = create_parser()
    
    args = parser.parse_args()
    main(args)
    
