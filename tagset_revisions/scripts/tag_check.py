import json
import argparse
import subprocess
import io



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
    parser = argparse.ArgumentParser(description='Script for validating tags within a corpus. Needs both a corpus file and a json tagset file.')
    parser.add_argument('--tagset', '-t', required=True, help='Choose a tagset for baseline')
    parser.add_argument('--input', '-i', required=True, help='Input file')

    args = parser.parse_args()
    process = subprocess.Popen(['bash', 'get_unique_tags.sh',args.input], stdout=subprocess.PIPE)

    
    with io.TextIOWrapper(process.stdout, encoding='utf-8') as text:
        tag_list = [tag.strip('\n') for tag in text.readlines()]

    with open(args.tagset) as j_file:
        tag_dict = json.load(j_file)

    illegal_tags = []
    for tag in tag_list:
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
