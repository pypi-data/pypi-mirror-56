#!/bin/bash

VARIANTS=$1

python3 var_to_hg19.py ${VARIANTS} | sort -k1,1 -k2,2n> ${VARIANTS}.bed
awk 'BEGIN{FS=OFS="\t"} {print $1,$2-15,$3+15,$4}' ${VARIANTS}.bed > ${VARIANTS}.15bp_buffer.bed
bedtools getfasta -fi /home/joshchiou/references/ucsc.hg19.fasta -bed ${VARIANTS}.15bp_buffer.bed -fo ${VARIANTS}.20bp_buffer.fa
fimo --bgfile --motif-- --text --thresh 1e-4 --max-strand --parse-genomic-coord --verbosity 1 /home/joshchiou/references/combined.motif_database.meme ${VARIANTS}.20bp_buffer.fa \
	| awk 'BEGIN{FS=OFS="\t"} NR>1 {print $3,$4,$5,$1,$8,$6}' \
	| bedtools intersect -a ${VARIANTS}.bed -b - -wa -wb \
	> ${VARIANTS}.vars_motifs.bed

python3 find_disrupted_motifs.py ${VARIANTS}.vars_motifs.bed \
	| awk '$11 <= 1.0' \
	| bedtools merge -i - -c 4,8 -o distinct \
	> ${VARIANTS}.vars_motifs.disrupted.bed
