rm temp temp2 plot2.txt
i=0
for file in ./data/*.tsv; do
    awk -F $'\t' '{print $2 > "temp"}' $file
    awk '{print NF > "temp2"}' temp
    cat temp2 >> plot2.txt
    echo $i
    i=$((i+1))
done

python3 plot2.py

rm temp temp2 plot2.txt
