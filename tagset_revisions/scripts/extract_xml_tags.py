
import argparse

import xml.etree.ElementTree as ET
from sys import stdout

def gather_tags(fh):
    tree = ET.parse(fh)
    corpus = tree.getroot()

    tags = set()

    for text in corpus:
        for sent in text:
            for word in sent:
                pos = word.attrib['pos']
                tag = f"{pos} {word.attrib['msd']}"
                tags.add(tag)

    return sorted(list(tags))


if __name__ == "__main__":
    parser =  argparse.ArgumentParser(description='Script for splitting a corpus XML to smaller partitions')
    parser.add_argument('--input', '-i', required=True, help='path to input XML file')
    parser.add_argument('--output', '-o', help='path to output file')

    args = parser.parse_args()

    in_file = args.input

    # text_elements = extract_elements(in_file)

    tags = gather_tags(in_file)

    with open(args.output, 'w') if args.output else stdout as output:
        for tag_pair in tags:
            # output.write('\t'.join(tag_pair)+'\n')
            output.write(tag_pair+'\n')