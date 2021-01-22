import argparse
from sys import stdout

def build_tag_dict(fh, dest):
    is_tags = []
    fo_tags = []
    with open(fh, 'r') as file:
        for line in file.readlines():
            if line[0] == '#': continue
            is_tags.append(line.split()[0].strip())
            fo_tags.append(line.split()[1].strip())
    if dest == 'is':
        tag_dict = dict(zip(fo_tags, is_tags))
    elif dest == 'fo':
        tag_dict = dict(zip(is_tags, fo_tags))
    return tag_dict

def read_input(fh):
    """
    docstring
    """
    tags = []
    with open(fh, 'r') as file:
        for line in file.readlines():
            tags.append(line.strip())
    return tags

def run_conversion(tags, tdict):
    output_tags = []
    for tag in tags:
        new_tag = tdict.get(tag, 'MISSING')
        output_tags.append([tag, new_tag])
    return output_tags

if __name__ == "__main__":
    parser =  argparse.ArgumentParser(description='Script for converting list of icelanidc OTB tags to Faroese Sosialurin tags')
    parser.add_argument('--input', '-i', required=True, help='path to output file (otherwise written to stdout)')
    parser.add_argument('--output', '-o', help='path to output file (otherwise written to stdout)')
    parser.add_argument('--tag_file', '-t', required=True, help='path to tag file')
    parser.add_argument('--lang', '-l', required=True, choices=['is', 'fo'], help='destination language of conversion')

    args = parser.parse_args()

    dest_lang = args.lang  
    
    tag_dict = build_tag_dict(args.tag_file, dest_lang)

    input_tags = read_input(args.input)

    comparison = run_conversion(input_tags, tag_dict)
    
    with open(args.output, 'w') if args.output else stdout as output:
        for pair in comparison:
            if pair[1] == 'MISSING':
                output.write(pair[0]+'\t'+pair[1])  
                output.write('\n')

