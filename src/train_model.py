import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

BASE_DIR = "/home/aaru/projects/waf-ml/"
data_path = os.path.join(BASE_DIR, "data/processed_data.csv")
model_path = os.path.join(BASE_DIR, "models/waf_model.pkl")

# Loading the processed data
df = pd.read_csv(data_path)

# Selecting Features (X) and Target (y)
X = df[['length', 'char_count', 'percent_count', 'entropy', 'keyword_count']]
y = df['label']

# Splitting data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("🌲 Training the model on your custom dataset...")
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Performance Check
predictions = model.predict(X_test)
print(f"🎯 New Accuracy: {accuracy_score(y_test, predictions) * 100:.2f}%")
print(classification_report(y_test, predictions))

# Saving the model using absolute path
joblib.dump(model, model_path)
print(f"💾 High-accuracy model saved to: {model_path}")