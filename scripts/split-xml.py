import argparse
import os
import shutil
from collections import defaultdict
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

def extract_elements(file):
    """
    docstring
    """
    tree = ET.parse(file)
    corpus = tree.getroot()

    texts_by_date = defaultdict(list)

    for text in corpus:
        text_date = text.attrib['date']
        # for text in corpus:
        texts_by_date[text_date].append(text)
        # print(text.attrib)
        # input()

    return texts_by_date

def split_texts(text_list, num):
    
    text_list_len = len(text_list)-1
    output_list = []
    runner = 0
    part_runner = 0
    partition = []

    for text in text_list:
        partition.append(text)
        part_runner += 1
        if part_runner == num:
            output_list.append(partition)
            partition = []
            part_runner = 0
        elif runner == text_list_len:
            output_list.append(partition)
        runner += 1



    return output_list

def write_output_files(partition_dict, corpus_name):
    """Write partitioned XML to new files in output directory
    Creates specific output directory
    Removes output directory if it exists (under same name)

    Args:
        partition_dict (defaultdict): dict of partioned corpus, divided by date
        corpus_name (string): name of corpus being partitioned
    """
    
    # Output directory created
    out_path = args.corpus_name + '_split'
    if os.path.isdir(os.path.join(os.getcwd(), out_path)):
        print('deleted')
        shutil.rmtree(os.path.join(os.getcwd(), out_path))
    os.mkdir(out_path)

    # output XML written
    part_num = 0
    for text_date, texts in partition_dict.items():
        print('> Writing partition '+str(text_date))
        partition_name = corpus_name+'_'+str(text_date)
        output_path = os.path.join(out_path, partition_name)+'.xml'
        root = ET.Element('corpus')
        root.set('id', corpus_name)
        root.set('part', partition_name)
        # print(output_path)
        file = open(output_path, 'w')
        for text in texts:
            root.append(text)
        xml_string = ET.tostring(root, encoding='unicode', method='xml',)
        # reparsed = parseString(xml_string).toprettyxml(newl='', indent="\t")
        file.write(xml_string)
        file.close()


if __name__ == "__main__":

    parser =  argparse.ArgumentParser(description='Script for splitting a corpus XML to smaller partitions')
    parser.add_argument('--input', '-i', required=True, help='path to input tsv file')
    parser.add_argument('--text_count', '-c', required=False, default=1000, help='number of texts in each output file')
    # parser.add_argument('--output_folder', '-o', help='path to output folder')
    parser.add_argument('--corpus_name', '-name', required=False, default='fts', help='name of corpus being partitioned')
    
    args = parser.parse_args()

    partition_size = int(args.text_count)
    input_path = args.input
    corpus_name = args.corpus_name

    extracted_texts = extract_elements(input_path)

    # output_texts = split_texts(extracted_texts, partition_size)

    # print(len(text_list))
    # print(len(output_list))
    # for i in output_list:
    #     print(len(i))
    
    write_output_files(extracted_texts, corpus_name)

