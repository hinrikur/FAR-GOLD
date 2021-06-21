import os

class LengthError(Exception):
    pass

OUT = 0
IN = 1
POST_SCRIPT = 'sosialurin-post_script.wip.txt'
POST_MANUAL = 'sosialurin-post_manual.wip.txt'
DIRECTORY = "corpus"
NEW_FILE_NAME = "sosialurin-merged.wip.txt"
FULLPATH = os.path.abspath(os.path.join(os.path.dirname(__file__),'..',DIRECTORY))

def open_file(file_name, path):
    file_path = os.path.join(path, file_name)
    return open(file_path, 'r')

def save_file(tag_list, file_name, path):
    file_path = os.path.join(path, file_name)
    with open(file_path, "w") as f:
        f.writelines(tag_list)


def merge_files(out_file, in_file):
    out_file = out_file.readlines()
    in_file = in_file.readlines()
    if len(out_file) != len(out_file):
        raise LengthError('Files are not of same length')
    else:
        merged = [list(a) for a in zip(out_file, in_file)]
        return merged


def process_files(merged_list):
    count = 0
    for line in merged_list:
        if line[IN].endswith('\tx\n'):
            line[OUT] = line[IN][:-3] + '\n'
            count += 1
    print(f'{count} line(s) were altered')

    return [out_list for out_list, in_list in merged_list]

    
def main():
    script_file = open_file(POST_SCRIPT, FULLPATH)
    manual_file = open_file(POST_MANUAL, FULLPATH)
    merged_list = merge_files(script_file, manual_file)
    script_file.close()
    manual_file.close()

    out_list = process_files(merged_list)
    save_file(out_list, NEW_FILE_NAME, FULLPATH)
    

main()