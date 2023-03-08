#%%

import pandas as pd
from sklearn.preprocessing import LabelEncoder
import nltk
import re
from babel.numbers import parse_decimal
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 100)

# Download the necessary data files
nltk.download('punkt')

# read in data
path = '../../Facebook Marketplace Project/data/cars_total.csv'
data = pd.read_csv(path)
# data

# remove trash
data = data[~data['title'].isna()]
data.dropna(subset = ['title'])
remove_key_words = 'hot wheel|toy|disney|hotwheels|Pixar|Fast And Furious|auto hoy a crédito facil'
data = data[~data['title'].str.contains(remove_key_words, case=False)]
data
# title to lowercase
data['title'] = data['title'].str.lower()

# format and extract new columns
# extract year from title column
pattern_year = r'^(\d{4})'
pattern_door = r'(2d|4d)$'
# extract year and door style columns
data['year']  = data['title'].str.extract(pattern_year)
data['door']  = data['title'].str.extract(pattern_door)

data['door']  = data['door'].str.replace('D', '')
data['title'] = data['title'].str.replace(pattern_year, '').str.strip()
data['title'] = data['title'].str.replace(pattern_door, '').str.strip()

data['maker'] = data['title'].str.split().str[0]
data['title'] = data['title'].str.split(n = 1).str[1]

data['miles'] = data['mileage'].str.extract('(\d+)')
data['mileage'] = pd.to_numeric(data['miles'], errors='coerce') * 1000
data.drop(columns = ['miles'], axis = 0, inplace = True)
data = data[['year', 'maker', 'title','mileage', 'price', 'location','date_scraped','door', 'link']]

#### door column
data['door'] = data['door'].str[0]

#### price column
data = data.query("price != 'Free'")
data['price'] = data['price'].str.replace('[\$,]', '', regex=True)
data = data.dropna(subset = ['year'])

#### remove makers with less than 20 occurrences
maker_counts = data['maker'].value_counts()
data = data[data['maker'].isin(maker_counts[maker_counts >= 50].index.tolist())]
data

data.to_csv('C:/Users/porte/Desktop/coding/pmoody_resume/Facebook Marketplace Project/data/cars_clean.csv',index=False)
data

#%%

# data = data.dropna(subset = ['year'])

data['price'].hist(bins=30)

#%%
import altair as alt

# Create a histogram of price
histogram = alt.Chart(data.query("location=='Colorado Springs, CO'")).mark_bar().encode(
    x=alt.X('price', bin=True),
    y='count()'
)

# Add labels and title
histogram = histogram.properties(
    title='Histogram of Price',
    width=500,
    height=300
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
)

# Display the plot
histogram




#%%

####### prepare for model
from keras.preprocessing.text import Tokenizer

# Create a tokenizer object
tokenizer = Tokenizer()

# Fit the tokenizer on the title column
tokenizer.fit_on_texts(data['title'])

# Convert the title column to a sequence of numerical values
data['title_seq'] = tokenizer.texts_to_sequences(data['title'])
data


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

# %%


# %%
