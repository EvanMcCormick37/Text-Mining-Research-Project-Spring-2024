#imports
from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


#reading data into a dataframe for analysis

df = pd.read_csv('../data/wdms/tfidf/worldnewsapi/lemmed/text.csv',index_col=0)
#Here I will be using the lemmatized WorldNewsAPI text dataset, which includes a
#built-in sentiment score from the WorldNewsAPI website. I'll be attempting to 
#train a neural net model to predict this sentiment score.

#Making train and test datasets
matrix = pd.concat([df['sentiment'],df.iloc[:,4:]],axis=1)

validation_matrix = matrix.iloc[:500,:]
matrix = matrix.iloc[501:,:]

train, test = train_test_split(matrix,test_size=0.2)

train_labels = train['sentiment']
test_labels = test['sentiment']
validation_labels=validation_matrix['sentiment']

train = train.drop('sentiment',axis=1)
test = test.drop('sentiment',axis=1)
validation_matrix = validation_matrix.drop('sentiment',axis=1)

#Building the model

