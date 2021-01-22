
import argparse

import xml.etree.ElementTree as ET
from collections import defaultdict
from sys import stdout

def extract_elements(file):
    """
    docstring
    """
    tree = ET.parse(file)
    corpus = tree.getroot()

    texts = []

    for text in corpus:
        # for text in corpus:
        texts.append(text)
        # print(text.attrib)
        # input()

    return texts

def gather_info(elem_list):
    
    content_info = defaultdict(set)

    for elem in elem_list:
        for k,v in elem.attrib.items():
            content_info[k].add(v)

    return content_info


if __name__ == "__main__":
    parser =  argparse.ArgumentParser(description='Script for splitting a corpus XML to smaller partitions')
    parser.add_argument('--input', '-i', required=True, help='path to input XML file')
    parser.add_argument('--output', '-o', help='path to output file')

    args = parser.parse_args()

    in_file = args.input

    text_elements = extract_elements(in_file)

    content_info = gather_info(text_elements)

    with open(args.output, 'w') if args.output else stdout as output:
        for atrribute, data in content_info.items():
            output.write(atrribute + '\t' + ', '.join(sorted(list(data)))+'\n')