import re
import argparse
from sys import stdout


def regex_replacer(file):
    # Change VP to VPA
    file = re.sub(r"\tVP", r"\tVPA", file)

    # Switch order of last two adverb tags
    file = re.sub(r"\tD(\w)(\w)", r"\tD\2\1", file)

    # Add tags to imperative verbs (voice, tense and person)
    file = re.sub(r"\tVM(\w)", r"\tVMAP\g<1>2", file)

    # Add an infitive (I) tag for all VE tags and change medium
    # voice tag from E to M
    file = re.sub(r"\tVE\n", r"\tVIM\n", file)

    # Change VI tags to VIM (M for medium voice) for words
    # ending with "-st"
    file = re.sub(r"(st\tVI)\n", r"\1M\n", file)

    # Add a medium voice tag for tags paired with "-st" suffixed
    # words. Only changes tags consisting of 5 letters.
    file = re.sub(r"(st\tVN)(\w{3}\n)", r"\1M\2", file)

    # Add an active voice tag to all indicative verbs of length 5.
    file = re.sub(r"(\tVN)(\w{3}\n)", r"\1A\2", file)

    # Add an indicative mood to all other verbs in medium voice
    # and change medium tag (E) to (M)
    file = re.sub(r"\tVE(\w+)", r"\tVNM\1", file)

    # Add an active voice tag to all regular infinitive verbs
    file = re.sub(r"\tVI\n", r"\tVIA\n", file)

    # Adding a medium voice to all tags following past participle
    # verbs ending in "st" (needs to be manually checked to verify!)
    file = re.sub(r"(st\tVA)(\w+)", r"\1M\2", file)

    # Add an active voice to all past participle verbs that
    # have not been asigned a medium voice - (might need verification)
    file = re.sub(r"(\tVA)(\w{3}\n)", r"\1A\2", file)

    # Add tags to indeclinable adjectives, taking information
    # from preceding nouns
    file = re.sub(r"(\tS(\w{3}).*\n.*\t)AI", r"\1AI\2", file)

    # Adds tags to indeclinable adjectives, taking information
    # from the succeeding nouns. Also adds a positive degree.
    file = re.sub(r"\tAI(\n.*\tS(\w{3}).*)", r"\tAPI\2\1", file)

    # Change all SXP tags to S----P
    file = re.sub(r"\tSXP", r"\tS----P", file)

    # Add a hyphen where the article tag is missing in noun tags
    file = re.sub(r"\t(S\w{3})P", r"\t\1-P", file)

    # Change all "stak" words to DN
    file = re.sub(r"(\nstak\t).*\n", r"\1DN\n", file)


    return file



def main():
    parser = argparse.ArgumentParser(description='Modification script for tagged corpora', add_help=True)
    parser.add_argument('--input', '-i', required=True, help='Path to input corpora')
    parser.add_argument('--output', '-o', help='Output path')

    args = parser.parse_args()
    in_file = args.input
    
    with open(in_file, 'r') as f:
        file_text = f.read()
        altered_text = regex_replacer(file_text)

    with open(args.output, 'w') if args.output else stdout as output:
        output.write(altered_text)



if __name__ == '__main__':
    main()
