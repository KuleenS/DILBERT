# %%
import xml.etree.ElementTree as ET
import os
import argparse

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', '-m', help='the data type we are using', choices=['Chemical', 'Disease', 'all'])
    parser.add_argument('--path', '-p', help='the output path')
    return parser
# %%
def process_data(data: str, mode: str, output_path: str):
    tree = ET.parse(data)
    root = tree.getroot()
    for doc in root.findall('document'):
        id = doc.find('id').text
        file_name = os.path.join(output_path, f"{id}.concept")
        with open(file_name, 'w') as f:
            for passage in doc.findall('passage'):
                for annotation in passage.findall('annotation'):
                    infon_tags = annotation.findall('infon')
                    type = infon_tags[0].text
                    tag = infon_tags[1].text

                    if tag!="-1":
                        if tag=="IndividualMention":
                            tag = infon_tags[2].text
                        elif tag=="CompositeMention":
                            tag = infon_tags[2].text.replace("|", ",")

                        location_tag = annotation.find('location')
                        offset = int(location_tag.get('offset'))
                        length = int(location_tag.get('length'))
                        end = offset+length

                        text = annotation.find('text').text
                        if mode=="all":
                            f.write(f'{id}||{offset}|{end}||{type}||{text}||{tag}\n')
                        elif mode=="Chemical" and type=="Chemical":
                            f.write(f'{id}||{offset}|{end}||{type}||{text}||{tag}\n')
                        elif mode=="Disease" and type=="Disease":
                            f.write(f'{id}||{offset}|{end}||{type}||{text}||{tag}\n')


def main(args):
    mode = args.mode
    output_path = args.path
    data = [
        '../data/CDR_Data/CDR.Corpus.v010516/CDR_DevelopmentSet.BioC.xml',
        '../data/CDR_Data/CDR.Corpus.v010516/CDR_TestSet.BioC.xml',
        '../data/CDR_Data/CDR.Corpus.v010516/CDR_TrainingSet.BioC.xml'
    ]

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for data_path in data: 
        process_data(data_path, mode, output_path)

if __name__=="__main__":
    parser = create_parser()
    args = parser.parse_args()

    main(args)
