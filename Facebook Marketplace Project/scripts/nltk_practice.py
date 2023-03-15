#%%

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

# Load the data
data = pd.read_csv("train.txt", header=None, names=["text"])
data
#%%
# Preprocess the text data
data["text"] = data["text"].str.lower().str.replace("[^a-z\s]+", "")

# Extract features using bag-of-words
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(data["text"])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, data["label"], test_size=0.2, random_state=42)

# Train a logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
