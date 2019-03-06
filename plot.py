import matplotlib.pyplot as plt

numComments = []

f = open('plot.txt', 'r')
for line in f:
    x = int(line)
    numComments.append(x)
    # if x >= 1000:
    #     numComments.append(x)

# print(len(numComments))
numComments.sort()
del numComments[-1]

print(len(numComments))
# print(numComments[0])
# print(numComments[len(numComments)-1])
plt.hist(numComments, bins='auto')
plt.xlabel('Number of Comments')
plt.ylabel('Frequency')
plt.title('Frequency of number of comments in each movie')
plt.show()
