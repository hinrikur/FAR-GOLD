#!/bin/bash

awk -F '\t' '{print $2}' ../corpus/sosialurin-revised.txt | sort | uniq | sed '/^$/d' |cat > ../corpus/sosialurin-unique_tags.txt