import argparse
import re
from sys import stdout

def read_tagset(fh):
    """
    docstring
    """
    tags = []
    with open(fh, 'r') as file:
        for line in file.readlines():
            tags.append(line.strip())
    return tags

def convert_class(t_string):
    """
    docstring
    """
    cat_map = {
        'n' : 'S',  # nouns
        'l' : 'A',  # adjectives
        'f' : 'P',  # pronouns
        't' : 'N',  # numerals
        's' : 'V',  # verbs
        'a' : 'D',  # adverbs
        'c' : 'C',  # conjunctions
        # 'a' : 'E',  # prepositions
        'a' : 'D',  # prepositions
        'x' : 'I',  # interjection
        'e' : 'F',  # foreign word
        'x' : 'X',  # unanalyzed word
        'g' : 'P',  # articles (to pronoun)
        'v' : 'W',
        'm' : 'M',
        'k' : 'T',
        'p' : 'K'
        }
    # print(t_string[0], cat_map.get(t_string[0]))
    t_string = cat_map.get(t_string[0], t_string[0]) + t_string[1:]
    # print(t_string)
    # input()
    return t_string

def convert_substring(t_string):
    """
    docstring
    """

    gender_map = { # nouns, adjectives
        'v' : 'F',  # femenine gender
        'k' : 'M',  # masculine gender
        'h' : 'N',  # neuter gender
        'x' : 'X',  # other/unspecified
        '-' : 'X',  # other/unspecified
        '1' : '1',  # 1st person
        '2' : '2',  # 2nd person
        '3' : '3',  # 3rd person
        }
    number_map = {
        'e' : 'S', # singular
        'f' : 'P'  # plural
        }
    case_map = { # Nouns, adjectives, past participles
        'n' : 'N', # nominative
        'o' : 'A', # accusative
        'þ' : 'D', # dative
        'e' : 'G'  # genetive
        }
    declension_map = { # Adjectives
        's' : 'S', # strong declension
        'v' : 'W', # week declension
        'o' : 'I'  # indeclinable
        }
    degree_map = { # Adjectives, adverbs
        'f' : 'P', # positive
        'm' : 'C', # comparative
        'e' : 'S'  # superlative
        }
    subcategory_map = { # pronouns
        'a' : 'D', # demonstrative pronoun
        'b' : 'B',
        'e' : 'E',
        'o' : 'I', 
        'p' : 'P', 
        's' : 'Q', 
        't' : 'R', 
        }
    # mood_map = {
    #     'ng' : 'I', # infinitive
    #     'b' : 'M',  # imperative
    #     'fg' : 'N', # indicative
    #     'v' : 'S',  # subjunctive
    #     'l' : 'P',  # present participle
    #     'fm' : 'E', # 'medium'
    #     'þ' : 'A'   # past participle
    #     }
    mood_map = {
        'b' : 'M',
        'f' : 'N',
        'l' : 'P',
        'n' : 'I',
        'þ' : 'A',
        }    
    tense_map = { # verbs
        'n' : 'P', # present tense
        'þ' : 'A'  # past tense
        }
    num_cat_map = {
        'f' : 'C', 
        'a' : 'O', 
        'p' : 'P', 
        'o' : 'R', 
    }
    category_case_governor_map = { # adverbs, prepositions
        'a' : 'N', # does not govern case
        'f' : 'G', # governs case
        }
    adverb_map = {
        'a' : 'N', # does not govern case
        'f' : 'G', # governs case
        'm' : 'C', # comparative
        'e' : 'S',  # superlative
        'u' : 'I'
        }
    category_conj_map = { # conjunctions
        'n' : 'I', # infinitive marker 'at'
        't' : 'R'  # relative conjunction
        }
    proper_nown_map = { # only proper nouns
        's' : 'P', # proper noun
        's' : 'L' # location (generalized 's' for icelandic)
        }
    abbr_cat_map = {
        's' : 'S',
        't' : 'T',
    }
    punct_cat_map = {
        'l' : 'E',
        'k' : 'C', 
        'g' : 'Q', 
        'a' : 'O',
    }

    new_tag = t_string

    # Nouns
    if t_string.startswith('S'):
        if re.search(r'---', t_string):
            new_tag = 'SP'
        else:
            new_tag = ''.join([
                            t_string[0],
                            gender_map[t_string[1]], 
                            number_map[t_string[2]], 
                            case_map[t_string[3]], 
                            t_string[4:]
                            ])
        
        if re.search(r'[g-]s?$', new_tag):
            new_tag = re.sub(r'g$', 'A', new_tag)
            new_tag = re.sub(r'gs$', 'AP', new_tag)
            new_tag = re.sub(r'-s$', 'P', new_tag)

    # Adjectives
    elif t_string.startswith('A'):
        new_tag = ''.join([
                            t_string[0],
                            degree_map[t_string[5]],
                            declension_map[t_string[4]],
                            gender_map[t_string[1]],
                            number_map[t_string[2]],
                            case_map[t_string[3]]
                            ])
    # Prounouns
    elif t_string.startswith('P'):
        # Articles (per OTB tags)
        if len(t_string) == 4:
            new_tag = ''.join([
                            t_string[0],
                            gender_map[t_string[1]],
                            number_map[t_string[2]],
                            case_map[t_string[3]],
                            ])
        # All other
        else:
            new_tag = ''.join([
                            t_string[0],
                            subcategory_map[t_string[1]],
                            gender_map[t_string[2]],
                            number_map[t_string[3]],
                            case_map[t_string[4]],
                            ])
    # Numerals
    elif t_string.startswith('N'):
        if len(t_string) == 2:
            new_tag = ''.join([
                            t_string[0],
                            num_cat_map[t_string[1]],
                            ])
        else:
            new_tag = ''.join([
                            t_string[0],
                            num_cat_map[t_string[1]],
                            gender_map[t_string[2]],
                            number_map[t_string[3]],
                            case_map[t_string[4]]
                            ])
    # Verbs
    elif t_string.startswith('V'):
        if t_string[1] == 'þ':
            # if re.search(r'm', t_string):
            #     new_tag = '-'
            # else:
            new_tag = ''.join([
                        t_string[0],
                        mood_map[t_string[1]],
                        gender_map[t_string[3]],
                        number_map[t_string[4]],
                        case_map[t_string[5]]
                        ])
        else:
            if re.search(r'(bm|V(s|nm))', t_string):
                new_tag = '-'
            elif len(t_string) == 3:
                new_tag = ''.join([
                                t_string[0],
                                mood_map[t_string[1]]
                                ])
            elif re.search(r'm', t_string):
                new_tag = ''.join([
                                t_string[0],
                                'E',
                                tense_map[t_string[5]],
                                number_map[t_string[4]],
                                # case_map[t_string[5]]
                                t_string[3]
                                ])
            else:
                new_tag = ''.join([
                                t_string[0],
                                'N',
                                tense_map[t_string[5]],
                                number_map[t_string[4]],
                                t_string[3]
                                ])
    elif t_string.startswith('D'):
        if re.search(r'[þos]', t_string):
            new_tag = '-'
        elif len(t_string) == 3:
            new_tag = ''.join([
                            t_string[0],
                            degree_map[t_string[2]],
                            category_case_governor_map[t_string[1]],
                            ])
        else:
            new_tag = ''.join([
                            t_string[0],
                            adverb_map[t_string[1]]
                            ])
    elif t_string.startswith('C'):
        if len(t_string) == 2:
            new_tag = ''.join([
                            t_string[0],
                            category_conj_map[t_string[1]]
                            ])  
    elif t_string.startswith('T'):
        new_tag = ''.join([
                        t_string[0],
                        abbr_cat_map[t_string[1]]
                        ])
    elif t_string.startswith('K'):
        new_tag = ''.join([
                        t_string[0],
                        punct_cat_map[t_string[1]]
                        ])
    return new_tag


def run_conversions(tag_list):
    new_tags = []
    for tag in tag_list:
        new_tag = convert_class(tag)
        new_tag = convert_substring(new_tag)
        new_tags.append(new_tag)
    return new_tags

if __name__ == "__main__":
    
    parser =  argparse.ArgumentParser(description='Script for converting list of icelanidc OTB tags to Faroese Sosialurin tags')
    parser.add_argument('--input', '-i', required=True, help='path to input file')
    parser.add_argument('--output', '-o', help='path to output file (otherwise written to stdout)')
    
    args = parser.parse_args()

    tagset = read_tagset(args.input)

    new_tagset = run_conversions(tagset)

    comparison = zip(tagset, new_tagset)
    
    with open(args.output, 'w') if args.output else stdout as output:
        for pair in comparison:
            output.write(pair[0]+'\t'+pair[1])  
            output.write('\n')


