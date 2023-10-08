#!/bin/bash
# https://fosspost.org/divide-pdf-small-chunks-linux-command-line/

set -ex

file=$1
pagesper=$2
outdir=$3

# if [ ! -z ${pagesper+x} ]; then "pagesper not defined: $pagesper"; fi
# if [ ! -z ${file+x} ]; then "file not defined $file"; fi

number=$(pdfinfo "$file" 2> /dev/null | grep "Pages" | awk '{print $2}')

count=$(((number+pagesper-1)/pagesper))
filename=$(basename ${file%.pdf})

counter=0
while [ "$count" -gt "$counter" ]; do
	start=$((counter*pagesper + 1));
	end=$((start + pagesper - 1));
	if [ $end -gt $number ]; then
		end=$number
	fi

	counterstring=$(printf %01d "$counter")
	pdftk "$file" cat "${start}-${end}" output "${outdir}${filename}_${counterstring}.pdf"
	counter=$((counter + 1))
done
