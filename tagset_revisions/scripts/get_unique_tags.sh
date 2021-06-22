#!/bin/bash

awk -F '\t' '{print $2}' $1 | sort | uniq | sed '/^$/d'