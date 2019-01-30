awk '{print $1}' movies.txt > plot.txt
python3 plot.py
rm plot.txt
