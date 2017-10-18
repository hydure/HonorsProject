# TODO: Train RNN with data from ibcData.pkl
# Got idea on how to use a custom dataset from https://stackoverflow.com/questions/41322243/how-to-use-keras-rnn-for-text-classification-in-a-dataset
# which is based on code from this webpage: https://machinelearningmastery.com/sequence-classification-lstm-recurrent-neural-networks-python-keras/
# Assumed specific batch size and number of epochs from https://stackoverflow.com/questions/35050753/how-big-should-batch-size-and-number-of-epochs-be-when-fitting-a-model-in-keras

# LSTM RNN with dropout for sequence classification
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
import pandas as pd
from sklearn.cross_validation import train_test_split
import pickle

# fix random seed for reproducibility
numpy.random.seed(7)

#TODO: put url here
url = ''
sms = pd.read_table(url, header=None, names=['label', 'message'])

# convert label to a numerical variable
sms['label_num'] = sms.label.map({'liberal':0, 'conservative':1})
X = sms.message
y = sms.label_num
print(X.shape)
print(y.shape)

# load the dataset but only keep the top n words, zero the rest
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
top_words = 5000

# truncate and pad input sequences
max_review_length = 500
X_train = sequence.pad_sequences(X_train, maxlen=max_review_length)
X_test = sequence.pad_sequences(X_test, maxlen=max_review_length)

# create the model
embedding_vecor_length = 32
model = Sequential()
model.add(Embedding(top_words, embedding_vecor_length, input_length=max_review_length, dropout=0.2))
model.add(LSTM(100, dropout_W=0.2, dropout_U=0.2))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())
model.fit(X_train, y_train, nb_epoch=3, batch_size=64)

# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))