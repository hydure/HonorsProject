# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from sklearn.feature_extraction.text import CountVectorizer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
import re, _pickle , csv

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory
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
lib, con, neutral] = cPickle.load(open('ibcData.pkl', 'rb'))
data = pd.read_csv(URL, header=None, names=['label', 'message'], sep=SEPERATOR)
print(data[0])
