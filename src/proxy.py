import os
import joblib
import pandas as pd
import webbrowser 
from flask import Flask, request, abort, render_template_string
from features import extract_features

app = Flask(__name__)

# --- CONFIGURATION ---
BASE_DIR = "/home/aaru/projects/waf-ml/"
MODEL_PATH = os.path.join(BASE_DIR, "models/waf_model.pkl")

# --- LOAD THE BRAIN ---
model = joblib.load(MODEL_PATH)
print(f"🧠 ML Model (98.97% Accuracy) loaded successfully.")

# --- THE NEW INTERACTIVE DASHBOARD ---
@app.route('/')
def home():
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>WAF Gateway Dashboard</title>
            <style>
                body { background-color: #0d1117; color: #c9d1d9; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                .container { text-align: center; border: 1px solid #30363d; padding: 40px; border-radius: 12px; background: #161b22; width: 500px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
                h1 { color: #58a6ff; margin-bottom: 5px; }
                .status { color: #238636; font-size: 0.9em; margin-bottom: 25px; }
                .search-box { display: flex; gap: 10px; margin-top: 20px; }
                input[type="text"] { flex-grow: 1; padding: 12px; border-radius: 6px; border: 1px solid #30363d; background: #010409; color: white; outline: none; }
                input[type="text"]:focus { border-color: #58a6ff; }
                button { padding: 12px 20px; border-radius: 6px; border: none; background: #238636; color: white; cursor: pointer; font-weight: bold; }
                button:hover { background: #2ea043; }
                .footer { margin-top: 30px; font-size: 0.8em; color: #484f58; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🛡️ WAF Gateway</h1>
                <div class="status">● RF-MODEL ACTIVE [98.97% ACCURACY]</div>
                <p>Enter a URL or search query to begin secure browsing:</p>
                <form onsubmit="event.preventDefault(); window.location.href = '/' + document.getElementById('query').value;" class="search-box">
                    <input type="text" id="query" placeholder="e.g., google.com/search?q=cybersecurity" required>
                    <button type="submit">Verify & Go</button>
                </form>
                <div class="footer">Arjun Kallatt | B.Tech CSE | LPU</div>
            </div>
        </body>
        </html>
    """)

# --- THE SECURITY GATEKEEPER ---
@app.before_request
def inspect_request():
    url_to_check = request.full_path
    
    # 1. Whitelist favicon and internal root
    if "favicon.ico" in url_to_check:
        return "Icon skipped", 200
    if url_to_check in ["/", "/?"]:
        return

    # 2. Extract features and predict
    features = extract_features(url_to_check)
    features_df = pd.DataFrame([features], 
                               columns=['length', 'char_count', 'percent_count', 'entropy', 'keyword_count'])
    
    prediction = model.predict(features_df)
    
    if prediction[0] == 1:
        print(f"🚨 BLOCKED ATTACK: {url_to_check}")
        abort(403)
    else:
        # --- DYNAMIC FORWARDING ---
        clean_path = request.path.lstrip('/')
        if not clean_path.startswith(('http://', 'https://')):
            target_url = f"https://{clean_path}"
        else:
            target_url = clean_path

        if request.query_string:
            target_url += f"?{request.query_string.decode('utf-8')}"

        print(f"✅ SAFE: Forwarding -> {target_url}")
        webbrowser.open_new_tab(target_url)
        
        return render_template_string("""
            <body style="background-color: #0d1117; color: #c9d1d9; font-family: sans-serif; text-align: center; padding-top: 100px;">
                <h2 style="color: #238636;">✔️ Security Verified</h2>
                <p>ML inspection complete. Redirecting...</p>
                <script>setTimeout(function(){ window.location.href = '/'; }, 1500);</script>
            </body>
        """)

if __name__ == '__main__':
    print('🚀 WAF Dashboard Live on http://127.0.0.1:8080')
    app.run(port=8080, debug=False)