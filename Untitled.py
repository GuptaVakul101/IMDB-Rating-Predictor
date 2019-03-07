#!/usr/bin/env python
# coding: utf-8

# In[30]:


import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
import gensim
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, GRU
from keras.layers.embeddings import Embedding
from keras.initializers import Constant
import numpy as np
from tensorflow.python.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from sklearn import model_selection


# In[2]:


punctuations = list(string.punctuation)
stop = stopwords.words('english')
dummy_stop = []
for word in stop:
    dummy = word[0].upper()+word[1:]
    dummy_stop.append(dummy)
stop = stop+dummy_stop
print(stop)


# In[3]:


reviews = []
rating = []
with open('all_reviews.tsv','r') as fp:
    lines=fp.readlines()

count=0
for line in lines:
    if count > 100:
        break
    words=word_tokenize(line)
    for i in range(len(words)):
        dummy=""
        for j in range(len(words[i])):
            if not words[i][j] in punctuations:
                dummy += words[i][j]
        words[i] = dummy
    clean_words=[w for w in words if not w in stop]
    rating.append(clean_words[len(clean_words)-1])
    clean_sym_words = [w for w in clean_words if w.isalpha()]
    reviews.append(clean_sym_words[0:len(clean_sym_words)-1])
    
    count += 1

print(reviews[0:5])
print(rating[0:5])


# In[4]:


# Using Google pre-trained word2vec embeddings
model = gensim.models.KeyedVectors.load_word2vec_format('./model/GoogleNews-vectors-negative300.bin', binary=True)


# In[5]:


# model.most_similar('horrible')


# In[6]:


# #save model
# filename = "./embedding_word2vec.txt"
# model.save_word2vec_format(filename, binary = False)


# In[7]:


# embeddings = {}
# fp = open("embedding_word2vec.txt")
# for line in fp:
#     val = line.split()
#     word = val[0]
#     vector_coefs = np.asarray(val[1:])
#     embeddings[word]=vector_coefs
# print(embeddings)
# fp.close()


# In[18]:


tokenized_obj = Tokenizer()
tokenized_obj.fit_on_texts(reviews)
sequences = tokenized_obj.texts_to_sequences(reviews)
# print(sequences)
word_index = tokenized_obj.word_index
# print(word_index)
# print(len(word_index))
# print(len(word_index))
maxLength = 0
for review in sequences:
    if maxLength < len(review):
        maxLength = len(review)
# print(maxLength)


# In[24]:


review_pad = pad_sequences(sequences, maxlen = maxLength)
rating = np.asarray(rating)
print(rating)


# In[39]:


EmbeddingDim = 300
num_words = len(word_index)+1
embedding_matrix  = np.zeros((num_words, EmbeddingDim))
for word, i in word_index.items():
    embedding_vector = embeddings.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector
print(num_words)


# In[27]:


# print(len(rating))
rating_matrix = np.zeros((len(rating), 11))
for i in range(len(rating)):
    rating_matrix[i][int(rating[i])] = 1
# print(rating_matrix)


# In[38]:


train_model = Sequential()
embedding_layer = Embedding(num_words, EmbeddingDim, embeddings_initializer = Constant(embedding_matrix), input_length = maxLength, trainable = False)
train_model.add(embedding_layer)
train_model.add(GRU(units = 100))
train_model.add(Dense(11,activation = 'sigmoid'))
train_model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])


# In[35]:


X_train, X_test, Y_train, Y_test = model_selection.train_test_split(review_pad, rating_matrix)
# print(X_train.shape)
# print(Y_train.shape)
train_model.fit(X_train, Y_train, epochs = 3, batch_size = 32)


# In[36]:


loss, accuracy = train_model.evaluate(X_test, Y_test)
print(accuracy*100)


# In[ ]:




