#%%

import pandas as pd
from sklearn.preprocessing import LabelEncoder
import nltk
import re
pd.set_option('display.max_rows', 100)

# Download the necessary data files
nltk.download('punkt')

# read in data
path = '../../Facebook Marketplace Project/data/cars_total.csv'
data = pd.read_csv(path)
data

data = data[~data['title'].isna()]
data.dropna(subset = ['title'])
remove_key_words = 'hot wheel|toy|disney|hotwheels|Pixar|Fast And Furious|auto hoy a crédito facil'
data = data[~data['title'].str.contains(remove_key_words, case=False)]

# extract year from title column
pattern_year = r'^(\d{4})'
pattern_door = r'(2D|4D)$'
# extract year and door style columns
data['year']  = data['title'].str.extract(pattern_year)
data['door']  = data['title'].str.extract(pattern_door)

data['door']  = data['door'].str.replace('D', '')
data['title'] = data['title'].str.replace(pattern_year, '').str.strip()
data['title'] = data['title'].str.replace(pattern_door, '').str.strip()

data['maker'] = data['title'].str.split().str[0]
data['title'] = data['title'].str.split(n = 1).str[1]


data = data.dropna(subset = ['year'])

data
# data.drop(['link'], axis=0)
# data.groupby(['maker']).agg(sum)

#%%


data_top_makers = data.groupby('maker').size().reset_index().sort_values(by = 0, ascending=False).reset_index(drop=True).head(50)
joined = pd.merge(data, data_top_makers, on='maker', how='inner').reset_index(drop=True)
print(joined.tail())

#%%

data.head(50)

#%%


# Define a function to tokenize and label encode the text
def label_encode_text(text):
    # Remove non-alphanumeric characters
    text = re.sub(r'\W+', ' ', text)
    # Tokenize the text using word_tokenize()
    tokens = nltk.word_tokenize(text)
    # Encode the tokens using LabelEncoder
    le = LabelEncoder()
    encoded_tokens = le.fit_transform(tokens)
    return encoded_tokens.tolist()

# Encode the 'Text' column
data['encoded'] = data['title'].apply(label_encode_text)

data
# # %%
# import pandas as pd
# import re

# # Create a sample DataFrame with a 'Title' column
# data = pd.DataFrame({'title': ['1998 Mitsubishi Eclipse GS Coupe 2D',
#                              'Ford Mustang GT Convertible 2010',
#                              'Honda Civic LX Sedan 2015',
#                              '2012 Chevrolet Camaro SS Coupe',
#                              'Toyota Corolla LE 2009']})

# # Define a regular expression pattern to match a four-digit year at the beginning of a string

# # Use str.extract() to extract the year from the 'Title' column


# # Print the updated DataFrame
# print(data)

# # %%

# %%
