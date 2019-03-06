i=0
for file in ./data/*.tsv; do
    awk -F $'\t' '{ if($3 != "") {print $2"\t"$3 > "temp"}}' $file
    awk '{if(NF>50){print $0 > "temp2"}}' temp
    name=${file:7}
    mv temp2 ./data2/$name
    echo $i
    i=$((i+1))
done

rm temp temp2
