# TODO: Train RNN until fairly accurate (80% without overfitting) and pickle it
# Maybe a better version? https://machinelearnings.co/tensorflow-text-classification-615198df921
# Got idea on how to use a custom dataset from https://stackoverflow.com/questions/412224/how-to-use-keras-rnn-for-text-classification-in-a-dataset
# which is based on code from this webpage: https://machinelearningmastery.com/sequence-classification-lstm-recurrent-neural-networks-python-keras/
# Assumed specific batch size and number of epochs from https://stackoverflow.com/questions/505075/how-big-should-batch-size-and-number-of-epochs-be-when-fitting-a-model-in-keras
# Asked how to tokenize the last part... https://stackoverflow.com/questions/46964090/training-rnn-with-lstm-nodes/46964768#46964768

# LSTM RNN with dropout for sequence classification
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from sklearn.model_selection import train_test_split
import numpy, pandas as pd

###################################### CONSTANTS #############################################

SEED = 7                        # Fixes random seed for reproducibility.
URL = 'ibcData.tsv'             # Specified dataset to gather data from.
SEPERATOR = '\t'                # Seperator the dataset uses to divide data.
RANDOM_STATE = 1                # Pseudo-random number generator state used for random sampling.
HIDDEN_LAYER_SIZE = 100         # Details the amount of nodes in a hidden layer.
TOP_WORDS = 5000                # Most used words in the dataset.
MAX_REVIEW_LENGTH = 500         # Char length of each text being sent in (necessary).
EMBEDDING_VECTOR_LENGTH = 2     # The specific Embedded later will have 2-length vectors to
                                # represent each word.
BATCH_SIZE = 64                 # Takes 64 sentences at a time and continually retrains RNN.
NUMBER_OF_EPOCHS = 2            # Fits RNN to more accurately guess the data's political bias.
DROPOUT = 0.2                   # Helps slow down overfitting of data (slower convergence rate)
FILE_NAME = 'finalizedModel.h5' # File LSTM RNN is saved to so it can be used for website

##############################################################################################

# Fix random seed for reproducibility
numpy.random.seed(SEED)


readData = pd.read_csv(URL, header=None, names=['label', 'message'], sep=SEPERATOR)

# Convert label to a numerical variable
tokenizer = Tokenizer(num_words=MAX_REVIEW_LENGTH)
tokenizer.fit_on_texts(readData.message)
X = numpy.array(tokenizer.texts_to_matrix(readData.message)) # Shape (None, 2)
readData['label_num'] = readData.label.map({'Liberal' : 0, 'Neutral': 0.5, 'Conservative' : 1})
Y = numpy.array(readData.label_num)  # Either 0.0, 0.5, or 1.0 depending on label mapped to


# Load the dataset into training and testing datasets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, random_state=RANDOM_STATE)

# Define and compile the model
model = Sequential()
model.add(Embedding(TOP_WORDS, EMBEDDING_VECTOR_LENGTH, input_length=MAX_REVIEW_LENGTH))
model.add(LSTM(HIDDEN_LAYER_SIZE))
model.add(Dropout(DROPOUT))
model.add(Dense(1, activation='sigmoid'))   # Layers deal with a 2D tensor, and output a 2D tensor
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())

# Fit the model
model.fit(X_train, Y_train, validation_data=(X_test, Y_test), epochs=NUMBER_OF_EPOCHS, batch_size=BATCH_SIZE)

# Final evaluation of the model
scores = model.evaluate(X_test, Y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))

# Save model
model.save(FILE_NAME)               # Creates a HDF5 file to save the whole model
print("Model saved.\n")             # (architecture, weights, and optimizer rate)