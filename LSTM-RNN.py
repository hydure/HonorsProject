# TODO: Train RNN with data from ibcData.pkl
# Maybe a better version? https://machinelearnings.co/tensorflow-text-classification-615198df9231
# Got idea on how to use a custom dataset from https://stackoverflow.com/questions/41322243/how-to-use-keras-rnn-for-text-classification-in-a-dataset
# which is based on code from this webpage: https://machinelearningmastery.com/sequence-classification-lstm-recurrent-neural-networks-python-keras/
# Assumed specific batch size and number of epochs from https://stackoverflow.com/questions/35050753/how-big-should-batch-size-and-number-of-epochs-be-when-fitting-a-model-in-keras
# Asked how to tokenize the last part... https://stackoverflow.com/questions/46964090/training-rnn-with-lstm-nodes/46964768#46964768

# LSTM RNN with dropout for sequence classification
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from sklearn.model_selection import train_test_split
import pickle, numpy, pandas as pd

###################################### CONSTANTS #############################################

SEED = 7                        # Fixes random seed for reproducibility.
URL = 'ibcData.tsv'             # Specified dataset to gather data from.
SEPERATOR = '\t'                # Seperator the dataset uses to divide data.
RANDOM_STATE = 1                # Pseudo-random number generator state used for random sampling.
TOP_WORDS = 5000                # Most used words in the dataset.
MAX_REVIEW_LENGTH = 500         # Length of each sentence being sent in (necessary).
EMBEDDING_VECTOR_LENGTH = 32    # The specific Embedded later will have 32-length vectors to
                                # represent each word.
BATCH_SIZE = 64                 # Takes 64 sentences at a time and continually retrains RNN.
NUMBER_OF_EPOCHS = 3            # Fits RNN to more accurately guess the data's political bias.
DROPOUT = 0.2                   # Helps slow down overfitting of data (slower convergence rate)

##############################################################################################

# fix random seed for reproducibility
numpy.random.seed(SEED)


readData = pd.read_csv(URL, header=None, names=['label', 'message'], sep=SEPERATOR)

# convert label to a numerical variable
tokenizer = Tokenizer(num_words=MAX_REVIEW_LENGTH)
tokenizer.fit_on_texts(readData.message)
X = numpy.array(tokenizer.texts_to_matrix(readData.message)) # shape (None, 32)
readData['label_num'] = readData.label.map({'Liberal' : 0, 'Neutral': 0.5, 'Conservative' : 1})
Y = numpy.array(readData.label_num)  # Either 0.0, 0.5, or 1.0 depending on label mapped to


# load the dataset into training and testing datasets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, random_state=RANDOM_STATE)

# create the model
model = Sequential()
model.add(Embedding(TOP_WORDS, EMBEDDING_VECTOR_LENGTH, input_length=MAX_REVIEW_LENGTH))
model.add(LSTM(100))
model.add(Dropout(DROPOUT))
model.add(Dense(1, activation='sigmoid'))   # Layers deal with a 2D tensor, and output a 2D tensor
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())
model.fit(X_train, Y_train, validation_data=(X_test, Y_test), epochs=NUMBER_OF_EPOCHS, batch_size=BATCH_SIZE)

# Final evaluation of the model
scores = model.evaluate(X_test, Y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))