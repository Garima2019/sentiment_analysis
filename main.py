import pandas as pd
import numpy as np
import re
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# Preprocess the data
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    return text

# Load the dataset
df = pd.read_csv('IMDB Dataset.csv', encoding='latin-1')
df['clean_review'] = df['review'].apply(clean_text)

#Convert Text → Numbers (Vectorization)
vectorizer = TfidfVectorizer(max_features=5000)
X= vectorizer.fit_transform (df['clean_review']).toarray()
y = df['sentiment']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2,random_state=42)


# Train the model
model = LogisticRegression()
model.fit(X_train,y_train)

# Make predictions
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

#test wth custome input
def predict_sentiment(review):
    text = clean_text(review)
    vector = vectorizer.transform([text]).toarray()
    return model.predict(vector)[0]

print(predict_sentiment("This product is amazing"))


#save model
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))


