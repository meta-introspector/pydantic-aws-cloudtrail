#!/bin/bash
#TGT=${1-output/visual/}
#mkdir -p ${TGT}
#for x in $(ls *.txt);
#do
echo filename $1
ollama run temp1 < $1 > ${1}.out1
#done
