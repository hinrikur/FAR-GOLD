import json
import os


TAGSETS_SCEMA = "tagsets"
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',TAGSETS_SCEMA))
schema_file = f'{PROJECT_PATH}/fo_tagset-revised_isl.json'

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
    test_tag = ''

    ex_tag = extend_tag(test_tag, tag_dict)

    print(ex_tag)

    # try:
    #     option = show_option(test_tag, tag_dict)
    # except IndexError:
    #     option = ERROR

    # print(option)
