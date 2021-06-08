import os, re

FILE_NAME = "sosialurin.wip.txt"
DIRECTORY = "corpus"
NEW_FILE_NAME = "sosialurin-post_script.wip.txt"
FULLPATH = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','corpus'))

def open_file():
    file_path = os.path.join(FULLPATH, FILE_NAME)
    return open(file_path, 'r')


def save_file(tag_list):
    file_path = os.path.join(FULLPATH, NEW_FILE_NAME)
    with open(file_path, "w") as f:
        f.write(tag_list)


def regex_replacer(file):
    # Change VP to VPA
    file = re.sub(r"\tVP", r"\tVPA", file)

    # Switch order of last two adverb tags
    file = re.sub(r"\tD(\w)(\w)", r"\tD\2\1", file)

    # Add tags to imperative verbs (voice, tense and person)
    file = re.sub(r"\tVM(\w)", r"\tVMAP\g<1>2", file)

    # Add an infitive (I) tag for all VE tags and change middle
    # voice tag from E to M
    file = re.sub(r"\tVE\n", r"\tVIM\n", file)

    # Add an indicative mood to all other verbs in middle voice
    # and change middle tag (E) to (M)
    file = re.sub(r"\tVE(\w+)", r"\tVNM\1", file)

    # Adding a middle voice to all tags following past participle
    # verbs ending in "st" (needs to be manually checked to verify!)
    file = re.sub(r"(st\tVA)(\w+)", r"\1M\2", file)

    # Add an active voice to all past participle verbs that
    # have not been asigned a middle voice - (might need verification)
    file = re.sub(r"(\tVA)([^M]{3})", r"\1A\2", file)

    # Add tags to indeclinable adjectives, taking information
    # from preceding nouns
    file = re.sub(r"(\tS(\w{3}).*\n.*\t)AI", r"\1AI\2", file)

    # Adds tags to indeclinable adjectives, taking inmormation
    # from the succeeding nouns
    file = re.sub(r"\tAI(\n\w*\tS(\w{3}).*)", r"\tAI\2\1", file)

    # Change all SXP tags to S----P
    file = re.sub(r"\tSXP", r"\tS----P", file)

    # Add a hyphen where the article tag is missing in noun tags
    file = re.sub(r"\t(S\w{3})P", r"\t\1-P", file)


    return file


def main():
    file_stream = open_file()
    file_text = file_stream.read()
    altered_text = regex_replacer(file_text)
    save_file(altered_text)

    file_stream.close()



if __name__ == '__main__':
    main()
