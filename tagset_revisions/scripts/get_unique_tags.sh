#!/bin/bash

awk -F '\t' '{print $2}' ../corpus/sosialurin-corpus_fixes.wip.txt | sort | uniq | sed '/^$/d' |cat > ../sosialurin-unique_tags.txt