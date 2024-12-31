TGT=output/visual/
mkdir -p ${TGT}
for x in $(ls *.txt);
do
    ollama run temp1 < ${x} > ${TGT}/${x}
done
