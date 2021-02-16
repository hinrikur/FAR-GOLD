


import argparse

from sys import stdout

import convert_opt

PUNCT = '!"#$%&\'()*+, -./:;<=>?@[\]^_`{|}~'

def read_input(fh):
    """
    docstring
    """
    tagged = []
    with open(fh, 'r') as file:
        for line in file.readlines():
            tagged.append(line.strip('\n').split())
            
    return tagged

def read_morphlex(fh):
    """ Saves words in ABLTagger morphlex file to set

    Args:
        fh (string): path to morphlex file
    Returns:
        set: set of words in morphlex file
    """

    morph_words = set()

    # added from morphlex file
    with open(fh, 'r') as file:
        for line in file.readlines():
            morph_words.add(line.split(';')[0])

    # manual additions, possibly not in file:
    morph_words.update([
        'ímeðan','líkasum','meðan','meðani','meðni','men','neman','og','ó','óast','óinn','sum','tí','tískil','tískjal','tóað','tóast','tóat','tóið','um','umenn','ummast','uttan','viss','darsum','dersum','altó','eins','ella','enn','enn','enn','enntá','enntó','annaðhvørt','antil','antin','fast','at','higar','áðrenn','hó','hóan','hóast','hógvið','hóið','hvørt','ið','innan','inntil','av','eins','fyrr','fyrsta','hvørki','so','síðan','til','tá','um','vissi','áðrenn', 'áraka', 'ífrá', 'ígegn', 'ígjøgnum', 'íhjá', 'íkring', 'ílendis', 'ímillum', 'ímót', 'ímóti', 'ímótur', 'bak', 'med', 'millum', 'mót', 'móti', 'mótur', 'mótvegis', 'nær', 'ón', 'pá', 'blant', 'sambært', 'til', 'um', 'umfram', 'umframt', 'umkring', 'undan', 'undir', 'úr', 'vegna', 'við', 'viður', 'viðvíkjandi', 'vinstrumegin', 'ymsumegin', 'yvir', 'øðruminni', 'eftir', 'andstøðis', 'andsýnis', 'aftrat', 'for', 'foruttan', 'at', 'frá', 'fyri', 'av', 'gjøgnum', 'handarumegin', 'hasumegin', 'heimanvert', 'heimarumegin', 'á', 'hesumegin', 'hinumegin', 'ábeint', 'hjá', 'hvørgumegin', 'hvørjumegin', 'høgrumegin', 'í',
        ])

    return morph_words


if __name__ == "__main__":
    
    parser =  argparse.ArgumentParser(description='Script for converting list of icelanidc OTB tags to Faroese Sosialurin tags')
    parser.add_argument('--input', '-i', required=True, help='path to input file')
    parser.add_argument('--output', '-o', help='path to output file (otherwise written to stdout)')
    parser.add_argument('--morphlex', '-M', help='path to ABLTagger morphlex file')
    
    
    args = parser.parse_args()

    tagged_fo = read_input(args.input)

    if args.morphlex:
        morphlex_words = read_morphlex(args.morphlex)

    tag_dict = convert_opt.build_tag_dict('tagsets/is-fo.tsv', 'is')


    with open(args.output, 'w') if args.output else stdout as output:
        for line in tagged_fo:
            if not line: 
                line.append('\n')
            else:
                line[1] = tag_dict.get(line[1])
                if line[0] in PUNCT:
                    pass
                elif args.morphlex:
                    if line[0].lower() not in morphlex_words:
                        line.append('UNKNOWN')
            output.write('\t'.join(line))
            if line[0] != '\n':
                output.write('\n')
                # print(f'{line[0]}\t{tag_dict.get(line[1])}\tUNKOWN')
        


    