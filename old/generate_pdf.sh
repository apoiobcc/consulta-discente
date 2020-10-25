#!/bin/bash

# this script merge the markdown templates with the coments,
# generating a markdown file for each discipline, and the 
# corresponding generated pdf will be in /reports

rm -r reports/
mkdir reports

echo 'generating pdfs'

for d in */ ; do
    cd $d

    echo $d
    # merge files
    cat name.txt ../ensino_remoto.md rmt_cmt.txt ../ensino_geral.md gen_cmt.txt > report.md
    # generate pdf from md
    pandoc -V geometry:margin=.3in -o ../reports/${d%?}.pdf report.md

    cd ..
done