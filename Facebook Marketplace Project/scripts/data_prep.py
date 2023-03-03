#%%

import pandas as pd
from sklearn.preprocessing import LabelEncoder
import nltk
import re

# Download the necessary data files
nltk.download('punkt')

# read in data
path = '../../Facebook Marketplace Project/data/cars_total.csv'
data = pd.read_csv(path)
data

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

# Print the updated DataFrame
print(data)

#%%
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
