mkdir output
for x in $(ls *.txt);
do
    ollama run temp1 < ${x} > output/${x}
done
