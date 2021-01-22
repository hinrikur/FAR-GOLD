
import re

def remove_verb_number(t_string):
    if re.search(r'V..P\d$', t_string):
        t_string = re.sub(r'\d', '', t_string)
    return t_string

if __name__ == "__main__":
    pass