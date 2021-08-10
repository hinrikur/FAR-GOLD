
import argparse
import os
import json
from tqdm import tqdm
import xml.etree.ElementTree as ET
from sys import stdout

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKING_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..', 'source_corpora', 'fts', 'fts_processed'))
POS_LIST = os.path.join(WORKING_DIR, 'pos-tag_pairs.json')


print(WORKING_DIR)

total_words = 0

def get_sentences(fh, sent_dict, total, num = 10000):

    global total_words
    
    tree = ET.parse(fh)
    corpus = tree.getroot()
    with open(POS_LIST, 'r') as f:
        pos_list = json.load(f)

    for txt in corpus:
        if total >= num:
            break
        total += 1
        for sent in txt:
            sent_id = sent.attrib['id']
            sent_dict[sent_id] = {
                'page': txt.attrib['page'],
                'date': txt.attrib['date'],
                'gender': txt.attrib['gender'],
                'authortype': txt.attrib['authortype'],
                'datefrom': txt.attrib['datefrom'],
                'timefrom': txt.attrib['timefrom'],
                'dateto': txt.attrib['dateto'],
                'timeto': txt.attrib['timeto']
            }
            token_tag = []
            for word in sent:
                total_words += 1
                token = word.text
                tag = ' '.join([word.attrib['pos'], word.attrib['msd']])
                token_tag.append((token, pos_list[tag]))

            sent_dict[sent_id]['token_tag'] = token_tag
    
    return extracted



if __name__ == "__main__":
    parser =  argparse.ArgumentParser(description='Script for splitting a corpus XML to smaller partitions')
    parser.add_argument('--input', '-i', required=True, help='path to input XML file directory')
    parser.add_argument('--output', '-o', required=True, help='path to output file')
    parser.add_argument('--number', '-n', required=True, help='number of sentences to be extracted')

    args = parser.parse_args()
    
    out_file = args.output
    in_dir = os.path.abspath(args.input)
    num_sents = int(args.number)

    print(in_dir)

    path_to_outfile = os.path.join(WORKING_DIR, out_file)


    # text_elements = extract_elements(in_file)

    extracted = {}
    sent_dict = extracted['sentences'] = {}
    total_sents = 0
    
    for file_name in tqdm(os.listdir(in_dir)):
        file_path = os.path.join(in_dir,file_name)
        if total_sents < num_sents:
            extracted_sents = get_sentences(file_path, sent_dict, total_sents, num_sents)
        else:
            break


    with open(path_to_outfile, 'w', encoding='utf-8') as f:
        json.dump(extracted_sents, f, ensure_ascii=False)


    print(f"Total words: {total_words}")
