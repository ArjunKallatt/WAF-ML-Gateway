import math
from collections import Counter

def calculate_entropy(text):
    if not text: 
        return 0
    # Count frequency of each character
    counts = Counter(text)
    probs = [count / len(text) for count in counts.values()]
    # Shannon Entropy Formula: -sum(p * log2(p))
    return -sum(p * math.log2(p) for p in probs)

def extract_features(url):
    url_lower = url.lower()
    
    # --- FEATURES ---
    length = len(url)
    
    # Count special characters
    special_chars = "';--<>\"()"
    char_count = sum(url.count(c) for c in special_chars)
    
    # NEW: Percent count (for encoded attacks)
    percent_count = url.count("%")
    
    # NEW: Entropy (Complexity)
    entropy = calculate_entropy(url)
    
    # Keywords
    keywords = ['select', 'insert', 'drop', 'script', 'union', 'waitfor', 'eval']
    keyword_count = sum(1 for word in keywords if word in url_lower)
    
    # Return 5 features now
    return [length, char_count, percent_count, entropy, keyword_count]

# --- TEST ---
print(f"Home Page [/]: {extract_features('/')}")
print(f"Attack URL: {extract_features('/?id=%27%20UNION')}")