import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

# Load the dataset
file_path = r'C:\Users\lenovo\Desktop\prernaaimlspamcheck-main\spamsentrypixalai\members\malicious_urls.csv'  # Use raw string (r'') to avoid escaping backslashes
df = pd.read_csv(file_path)

# Vectorize the URLs using TF-IDF
vectorizer = TfidfVectorizer(max_features=5000, analyzer='char', ngram_range=(3, 5))
X = vectorizer.fit_transform(df['url'])
y = df['type'].apply(lambda x: 1 if x != 'benign' else 0)  # Binary classification (malicious or not)

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the classifier
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save the vectorizer and model
joblib.dump(vectorizer, 'vectorizer.pkl')
joblib.dump(model, 'malicious_url_model.pkl')
print("Model and vectorizer saved!")

