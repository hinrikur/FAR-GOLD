##### Tag conversion from ABLTagger output to IcePaHC tagset
#
# Usage:
# python3 tag2ice.py
# (or python tag2ice.py if Python3 is the default)
# Reads icepach1.tsv and outputs icepach3.tsv with icetags added

from collections import namedtuple

Token = namedtuple('Token', ['word','tag','lemma'])

simple_replace = [('af','P'),
                  ('ct','C'),
                  ('c','CONJ'),
                  ('aa','ADV'),
                  ('e', 'FW'),
                  ('cn','TO'),
                  ('au','ADV'),
                  ('aae', 'ADVS'),
                  ('aam', 'ADVR'),
                  ('afm', 'ADVR'),
                  ('afe', 'ADVS'),
                  ('x', 'X'),
]

def icetag(tag, lemma):

    case = [('n', 'N'), ('o', 'A'), ('þ', 'D'), ('e', 'G')]
    degress = [('f', ''), ('m', 'R'), ('e', 'S')]
    number = [('e', ''), ('f', 'S')]
    aux = [('hafa', 'HV'), ('vera', 'BE'), ('verða', 'RD'), ('gera', 'DO')]
    aux2 = [('hafa', 'H'), ('vera', 'B'), ('verða', 'R'), ('gera', 'D')]
    modals1 = ('skulu', 'munu', 'mega', 'vilja', 'hljóta', 'þurfa', 'ætla')
    #modals2 = ('eiga', 'geta', 'verða', 'kunna')
    Neg = ('ekki', 'eigi', 'nei', 'né', 'ó')
    wadvs = ('hva', 'hvar', 'hvert', 'hví', 'því', 'þá', 'hversu', 'hvergi', 'hvernig', 'þegar', 'þar', 'hvorki', 'hvaðan', 'hve', 'hvenær')
    
    
    ###### Quantifiers
    if lemma == 'margur' and tag[3]=='þ':
        return 'Q-D'

    # do some specific replace commands
 
    ###### Complementizers

    if tag == 'c' and lemma == 'að':
        return 'C'
    
    ###### Verbs
    ## infinitive
    if tag.startswith('sn'):
        for x,y in aux:
            if lemma == x:
                return y
        for mv in modals1:
            if lemma == mv:
                return 'MD'
        if lemma != x and lemma != mv:
            return 'VB' 

    ## imperative
    if tag.startswith('sb'):
        for x,y in aux:
            if lemma == x:
                return y + 'I'
        for mv in modals1:
            if lemma == mv:
                return 'MDI'
        if lemma != x and lemma != mv:
            return 'VBI' 

    ## indicative
    if tag.startswith('sf'):
        for x,y in aux:
            if lemma == x and tag[5] == 'n':
                return y + 'PI'
            elif lemma == x and tag[5] == 'þ':
                return y + 'DI'
        for mv in modals1:
            if lemma == mv and tag[5] == 'n':
                return 'MDPI'
            elif lemma == mv and tag[5] == 'þ':
                return 'MDDI'
        if lemma != x and lemma != mv and tag[5] == 'n':
            return 'VBPI'
        elif lemma != x and lemma != mv and tag[5] == 'þ':
            return 'VBDI'

    """ if tag.startswith('sf') and lemma == 'hafa':
        return 'HVPI'    
    if tag.startswith('sf') and tag.endswith('n'):
        return 'VBPI' """

    
    ## subjunctive
    if tag.startswith('sv'):
        for x,y in aux:
            if lemma == x and tag[5] == 'n':
                return y + 'PS'
            elif lemma == x and tag[5] == 'þ':
                return y + 'DS'
        for mv in modals1:
            if lemma == mv and tag[5] == 'n':
                return 'MDPS'
            elif lemma == mv and tag[5] == 'þ':
                return 'MDDS'
        if lemma != x and lemma !=mv and tag[5] == 'n':
            return 'VBPS'
        elif lemma != x and lemma !=mv and tag[5] == 'þ':
            return 'VBDS'

    
    ## passive participle

    ## present participle
    if tag.startswith('sl'):
        for x,y in aux2:
            if lemma == x:
                return y + 'AG'
        for mv in modals1:
            if lemma == mv:
                return 'MAG'
        if lemma != x and lemma != mv:
            return 'VAG'

    ## past participle
    if tag.startswith('sþ'):
         ## vera
        if lemma == 'vera':
            if tag[5] == 'n':
                return 'BEN'
            for vabl, vice in case[1:4]:
                if tag[5] == vabl:
                    return 'BEN-' + vice
        ## gera    
        elif lemma == 'gera':
            if tag[5] == 'n':
                return 'DON'
            for gabl, gice in case[1:4]:
                if tag[5] == gabl:
                    return 'DON-' + gice
        ## hafa
        elif lemma == 'hafa':
            if tag[5] == 'n':
                return 'HVN'
            for habl, hice in case[1:4]:
                if tag[5] == habl:
                    return 'HVN-' + hice
        ## verða
        elif lemma == 'verða':
            if tag[5] == 'n':
                return 'RDN'
            for rdabl, rdice in case[1:4]:
                if tag[5] == rdabl:
                    return 'RDN-' + rdice
        
        ## modals
        for mv in modals1:
            if lemma == mv:
                if tag[5] == 'n':
                    return 'MDN'
                for rdabl, rdice in case[1:4]:
                    if tag[5] == rdabl:
                        return 'MDN-' + rdice
        
        if lemma not in modals1 and lemma not in ['hafa', 'vera','verða', 'gera']:
            if tag[5] == 'n':
                return 'VBN'
            for x, y in case[1:4]:
                if tag[5] == x:
                    return 'VBN-' + y
              
                
    
    ####### Numerals
    if tag.startswith('t'):
        for abl, ice in case:
            if tag.endswith(abl):
                return 'NUM-' + ice
    if tag.startswith('t') and not tag.endswith('n' or 'o' or 'þ' or 'e'):
        return 'NUM'
    
    ####### Articles
    if tag.startswith('g'):
        for abl, ice in case:
            if tag.endswith(abl):
                return 'D-' + ice 
    

    ####### Pronouns
    if tag.startswith('f'):
        for abl, ice in case:
            if tag.endswith(abl):
                return 'PRO-' + ice

    ####### Adjectives
    if tag.startswith('l'):
        for abl, ice in degress:
            if tag[5] == abl:
                for abl_case, ice_case in case:
                    if tag[3] == abl_case:
                        return "ADJ" + ice + '-' + ice_case
    
    ####### Nouns
    ## Proper nouns
    if tag.startswith('n') and tag.endswith('s'):
        if tag[1:4] == '---':
            return 'NPR'
        for m, n in number:
            if tag[2] == m:
                for e, f in case:
                    if tag[3] == e:
                        return 'NPR' + n + '-' + f
            elif tag[2] =='-':
                for e, f in case:
                    if tag[3] == e:
                        return 'NPR-' + f

    ## common nouns
    if tag.startswith('n') and (not tag.endswith('s')):
        for m, n in number:
            if tag[2] == m:
                for d, h in case:
                    if tag[3] == d:
                        return 'N' + n + "-" + h
        
    ## punctuations
    if tag.startswith('p'):
        return lemma  

    ## negation
    if lemma in Neg:
        return 'NEG'  

    ## wh-
    ## WADV
    if tag.startswith('a') and lemma in wadvs:
        return 'WADV'  

    ####### Simple replace
    # Replace all the tags from the simple replace list of binary tuples
    for before, after in simple_replace:
        if tag == before:
            return after
    



output = []
with open('icepahc1.tsv') as f:
    for line in f.read().splitlines():
        chunks = line.split()
        if(len(chunks)==3):
            
            token = Token(*chunks)
            _icetag = icetag(token.tag, token.lemma)
            line = '{}\t{}\t{}\t{}'.format(*token, _icetag)
            output.append(line)
    
with open('icepahc3.tsv','w') as f:
    f.write('\n'.join(output))
