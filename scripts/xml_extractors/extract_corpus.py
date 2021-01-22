
import argparse
import os

import xml.etree.ElementTree as ET
from collections import defaultdict
from sys import stdout

def gather_fields(fh):
    """
    docstring
    """
    tree = ET.parse(fh)
    corpus = tree.getroot()

    tokens, tags, lemmas = [], [], []

    for txt in corpus:
        for sent in txt:
            for word in sent:
                tokens.append(word.text)
                tags.append(word.attrib['msd'])
                lemmas.append(word.attrib['lemma'])
            tokens.append('')
            tags.append('')
            lemmas.append('')

    return tokens, tags, lemmas


if __name__ == "__main__":
    parser =  argparse.ArgumentParser(description='Script for splitting a corpus XML to smaller partitions')
    parser.add_argument('--input', '-i', required=True, help='path to input XML file')
    parser.add_argument('--output', '-o', required=True, help='path to output folder')

    args = parser.parse_args()
    
    output_container_name = 'fts_processed'
    output_path = os.path.join(args.output, output_container_name)

    try:
        os.mkdir(output_path)
    except FileExistsError:
        pass

    in_file = args.input


    # text_elements = extract_elements(in_file)

    tokens, tags, lemmas = gather_fields(in_file)


    # rawtext
    with open(os.path.join(output_path, 'fts.raw.txt'), 'w') if args.output else stdout as output:
        for token in tokens:
            # output.write('\t'.join(tag_pair)+'\n')
            output.write(token+'\n')

    with open(os.path.join(output_path, 'fts.tagged.txt'), 'w') if args.output else stdout as output:
        tagged = zip(tokens, tags)
        for line in tagged:
            # output.write('\t'.join(tag_pair)+'\n')
            output.write('\t'.join(line)+'\n')

    with open(os.path.join(output_path, 'fts.lem.txt'), 'w') if args.output else stdout as output:
        tag_lem = zip(tokens, tags, lemmas)
        for line in tag_lem:
            # output.write('\t'.join(tag_pair)+'\n')
            output.write('\t'.join(line)+'\n')