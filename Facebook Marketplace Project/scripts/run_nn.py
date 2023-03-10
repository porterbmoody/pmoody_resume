#%%
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np


pd.set_option('display.max_rows', 100)

path_clean = 'C:/Users/porte/Desktop/coding/pmoody_resume/Facebook Marketplace Project/data/cars_clean.csv'
data = pd.read_csv(path_clean)
data = data.dropna()

############### prepare data for model
#### create stopwords list for title
# Splitting each sentence into a list of words

# Creating a list of all words in the dataframe
all_words = []
for words_list in data['title'].str.split():
    all_words += words_list

# Creating a dictionary to count the frequency of each word
word_freq = {}
for word in all_words:
    if word not in word_freq:
        word_freq[word] = 1
    else:
        word_freq[word] += 1

# Creating a dataframe with the word and its frequency
word_freq_df = pd.DataFrame(list(word_freq.items()), columns=['word', 'frequency']).reset_index().sort_values(by = 'frequency',ascending=False)
stop_words = list(word_freq_df.query("frequency > 300")['word'])
stop_words

#%%
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

## encode maker column
le = LabelEncoder()
data['maker'] = le.fit_transform(data['maker'])

vectorizer = TfidfVectorizer(stop_words=stop_words, min_df=len(stop_words))
title_vectorized = vectorizer.fit_transform(data['title'])

feature_names = list(vectorizer.vocabulary_.keys())
print(feature_names)

#%%

# not_stop_words = [word for word in feature_names if word not in stop_words]
# print(not_stop_words)

VectorizedText=pd.DataFrame(title_vectorized.toarray(), 
                            columns=feature_names)
VectorizedText['originalText']=pd.Series(data['title'])
# VectorizedText = VectorizedText.loc[:, stop_words]
VectorizedText

data = pd.concat([data, VectorizedText], axis=1).dropna()
# data[feature_names] = title_vectorized.toarray()

# data = data.drop(not_stop_words, axis = 1)
data

#%%

# Split the data into training and testing sets
X = data.drop(columns = ['price','title','originalText'], axis = 1)
y = data['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the data using standardization
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# y_train = y_train.astype(float)
# y_test = y_test.astype(float)
X_train


#%%
################ Train neural network
from keras.models import Sequential
from keras.layers import Dense
from keras import backend as K
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import r2_score, mean_squared_error

def r_squared(y_true, y_pred):
    SS_res =  K.sum(K.square(y_true - y_pred)) 
    SS_tot = K.sum(K.square(y_true - K.mean(y_true))) 
    return ( 1 - SS_res/(SS_tot + K.epsilon()) )

model = Sequential()
model.add(Dense(64, activation='relu', input_dim=X.shape[1]))
model.add(Dense(128, activation='relu'))
model.add(Dense(1, activation='linear'))

model.compile(optimizer='adam', loss='mse',metrics=[r_squared])

model.fit(X_train, y_train, epochs=100, batch_size=64, validation_data=(X_test, y_test))

#%%
# extra trees
etr = ExtraTreesRegressor()
# fit the model on the data
etr.fit(X_train, y_train)


#%%

# make predictions on the testing data
y_pred = etr.predict(X_test)

# evaluate the performance of the model
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred, squared=False)

print('R-squared:', r2)
print('Mean Squared Error:', mse)
print('Root Mean Squared Error:', rmse)

#%%

