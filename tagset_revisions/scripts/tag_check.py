import json
import os


TAGSETS_DIR = 'tagsets'
CORPUS_DIR = 'corpus'
SCHEMA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', TAGSETS_DIR))
CORPUS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', CORPUS_DIR))

schema_file =  os.path.join(SCHEMA_PATH, 'fo_tagset-revised_isl.json')
taglist_file = os.path.join(CORPUS_PATH, 'sosialurin-unique_tags.txt')

with open(schema_file) as j_file:
    tag_dict = json.load(j_file)

def extend_tag(tag:str, tag_set:dict):

    expanded_tag = {}
    if not tag:
        return None

    if tag in tag_set['alternative']:
        expanded_tag['PoS'] = tag_set['alternative'][tag]
        return expanded_tag

    pos = tag[0]
    expanded_tag['PoS'] = tag_set['PoS'][pos]
    pos_list = tag_set[pos]

    if len(tag) > 1:
        index = 0
        pos_list = tag_set['forked_tags'][tag[:2]] if tag[:2] in tag_set['forked_tags'] else pos_list

        for letter in tag[1:]:
            expanded_tag[pos_list[index]] = tag_set[pos_list[index]][letter].capitalize()
            index += 1
    
    return expanded_tag

    
if __name__ == '__main__': 
    illegal_tags = []
    with open(taglist_file, 'r') as tag_file:
        for line in tag_file.readlines():
            tag = line.strip('\n')
            try:
                extend_tag(tag, tag_dict)
            except:
                illegal_tags.append(tag)
    
    if illegal_tags:
        print(f'The following {len(illegal_tags)} tag(s) are not permitted:')
        for tag in illegal_tags:
            print(tag)
    else:
        print("All tags are legal")
