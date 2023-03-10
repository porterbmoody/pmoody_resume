#%%

import pandas as pd
import nltk
import matplotlib.pyplot as plt
import altair as alt

alt.data_transformers.enable(max_rows=None)
pd.set_option('display.max_rows', 100)

# Download the necessary data files
nltk.download('punkt')

# read in data
path = '../data/cars_total.csv'
data = pd.read_csv(path)
data

#%%
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
# pattern_door = r'(2d|4d)$'
# extract year and door style columns
data['year']  = data['title'].str.extract(pattern_year)
# data['door']  = data['title'].str.extract(pattern_door)

# data['door']  = data['door'].str.replace('D', '')
data['title'] = data['title'].str.replace(pattern_year, '').str.strip()
# data['title'] = data['title'].str.replace(pattern_door, '').str.strip()

data['maker'] = data['title'].str.split().str[0]
data['title'] = data['title'].str.split(n = 1).str[1]

data['miles'] = data['mileage'].str.extract('(\d+)')
data['mileage'] = pd.to_numeric(data['miles'], errors='coerce') * 1000
data.drop(columns = ['miles'], axis = 0, inplace = True)
data = data[['year', 'maker', 'title','mileage', 'price','location','date_scraped', 'link']]

#### door column
# data['door'] = data['door'].str[0]
# data['door'] = data['door'].fillna(2)

#### price column
data = data.query("price != 'Free'")
data['price'] = data['price'].str.replace('[\$,]', '', regex=True)
data = data.dropna(subset = ['year'])

#### remove makers with less than 20 occurrences
maker_counts = data['maker'].value_counts()
data = data[data['maker'].isin(maker_counts[maker_counts >= 150].index.tolist())]
data

# data.to_csv('C:/Users/porte/Desktop/coding/pmoody_resume/Facebook Marketplace Project/data/cars_clean.csv',index=False)
data


data['mileage'] = pd.to_numeric(data['mileage'], errors='coerce')
data['price'] = pd.to_numeric(data['price'], errors='coerce')
data

#%%
# Drop rows with missing values
data = data.dropna(subset=['mileage'])
data = data.dropna(subset=['price'])

# drop unneeded columns
data = data.drop(['date_scraped', 'link'], axis = 1)

# remove trash rows
data = data[~data['title'].fillna('').str.contains('down payment', case=False)]
# remove rows where price is > 1,000,000 and mileage > 500,000
data = data.query("price < 1000000").query("mileage < 500000")

print(data.isna().sum())

data
#%%
data = (data.query("price < 500000")
        .query("mileage < 500000"))
data

#%%

alt.Chart(data.query("location == 'Phoenix, AZ' | location == 'Colorado Springs, CO'")).encode(
    x = "mileage",
    y = "price",
    color = "location"
).mark_point()


# #%%
# alt.Chart(data.query('maker == "nissan"')).encode(
#     x = "mileage",
#     y = "price"
# ).mark_point()

# #%%
# list(data['maker'].unique())

# #%%

# data.query('maker == "honda"').hist()

# #%%
# data.query('maker == "nissan"').hist()

# #%%
# data.query('maker == "chevrolet"').hist()

# #%%

data.drop(['location'], axis = 1, inplace = True)

# %%

data.to_csv('C:/Users/porte/Desktop/coding/pmoody_resume/Facebook Marketplace Project/data/cars_clean.csv',index=False)




# %%
