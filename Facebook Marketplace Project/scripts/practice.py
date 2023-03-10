#%%
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np



pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)

path_clean = 'C:/Users/porte/Desktop/coding/pmoody_resume/Facebook Marketplace Project/data/cars_clean.csv'
data = pd.read_csv(path_clean).head(20)
data = data.dropna()
data

#%%
############### prepare data for model
#### create stopwords list for title
# Splitting each sentence into a list of words
data['words'] = data['title'].str.split()

# Creating a list of all words in the dataframe
all_words = []
for words_list in data['words']:
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
stop_words = list(word_freq_df.query("frequency > 1")['word'])
stop_words


#%%
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

## encode maker column
le = LabelEncoder()
data['maker'] = le.fit_transform(data['maker'])

vectorizer = TfidfVectorizer(stop_words=stop_words)
title_vectorized = vectorizer.fit_transform(data['title'])
print(vectorizer.get_feature_names_out())

#%%
VectorizedText=pd.DataFrame(title_vectorized.toarray(), 
                            columns=vectorizer.get_feature_names_out())
VectorizedText['originalText']=pd.Series(data['title'])
VectorizedText
#%%
data[vectorizer.get_feature_names_out()] = title_vectorized.toarray()
data

#%%


X = data.drop(columns = ['price','title'], axis = 1)
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
