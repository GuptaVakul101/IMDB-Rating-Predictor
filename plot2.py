import matplotlib.pyplot as plt

numWords = []

f = open('plot2.txt', 'r')
for line in f:
    x = int(line)
    # numWords.append(x)
    if x > 50:
        numWords.append(x)

numWords.sort()

print(len(numWords))
plt.hist(numWords, bins='auto')
plt.xlabel('Number of Words')
plt.ylabel('Frequency')
plt.title('Frequency of number of words in each comment')
plt.show()
