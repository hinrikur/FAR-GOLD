import os
import argparse

from sys import stdout

import convert_opt

def read_corpus(fh):
    file_lines = []
    with open(fh, 'r') as file:
        for line in file.readlines():
            file_lines.append(line)
    return file_lines

def convert_corpus_lines(corpus, tdict):
    new_lines = []
    for line in corpus:
        if line == '\n':
            new_lines.append(line)
        else:
            token, tag = line.strip('\n').split()
            new_line = '\t'.join([token, tdict[tag]])+'\n'
            new_lines.append(new_line)
    return new_lines

if __name__ == "__main__":

    parser =  argparse.ArgumentParser(description='Script for converting list of icelanidc OTB tags to Faroese Sosialurin tags')
    parser.add_argument('--input', '-i', required=True, help='path to input file')
    parser.add_argument('--output', '-o', help='path to output file (otherwise written to stdout)')
    
    args = parser.parse_args()

    tag_dict = convert_opt.build_tag_dict('tagsets/is-fo.tsv', 'fo')
    
    corpus_lines = read_corpus(args.input)
    converted_corpus = convert_corpus_lines(corpus_lines, tag_dict)

    with open(args.output, 'w') if args.output else stdout as output:
        for line in converted_corpus:
            output.write(line)
            # output.write('\n')
            # if line == '\n':
            #     input()
