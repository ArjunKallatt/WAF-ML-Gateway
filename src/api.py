from flask import Flask, request, jsonify
from flask_cors import CORS  # You'll need: pip install flask-cors
import joblib
import pandas as pd
from features import extract_features
import os

app = Flask(__name__)
CORS(app) # Allows the Chrome extension to talk to this server

BASE_DIR = "/home/aaru/projects/waf-ml/"
model = joblib.load(os.path.join(BASE_DIR, "models/waf_model.pkl"))

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    url = data.get('url', '')
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    features = extract_features(url)
    features_df = pd.DataFrame([features], 
                               columns=['length', 'char_count', 'percent_count', 'entropy', 'keyword_count'])
    
    prediction = model.predict(features_df)[0]
    
    # Return 0 for Safe, 1 for Malicious
    return jsonify({
        "url": url,
        "prediction": int(prediction),
        "label": "Malicious" if prediction == 1 else "Safe"
    })

if __name__ == '__main__':
    app.run(port=5000)