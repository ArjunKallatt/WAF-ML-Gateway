import pandas as pd
import os
from features import extract_features

# Absolute path configuration
BASE_DIR = "/home/aaru/projects/waf-ml/"

def load_and_label(file_name, label):
    file_path = os.path.join(BASE_DIR, "data", file_name)
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found!")
        return pd.DataFrame()
        
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    temp_df = pd.DataFrame(urls, columns=['url'])
    temp_df['label'] = label
    return temp_df

print("📂 Loading custom URL files...")
good_df = load_and_label("goodqueries.txt", 0) # 0 = Safe
bad_df = load_and_label("badqueries.txt", 1)   # 1 = Attack

# Combine the dataframes
df = pd.concat([good_df, bad_df], ignore_index=True)
print(f"📊 Dataset Stats: {len(good_df)} Good, {len(bad_df)} Bad URLs.")

print("⚙️  Extracting features...")
features_list = df['url'].apply(extract_features)

# Creating the feature matrix
features_df = pd.DataFrame(features_list.tolist(), 
                           columns=['length', 'char_count', 'percent_count', 'entropy', 'keyword_count'])

# Combining features with labels
final_df = pd.concat([features_df, df['label']], axis=1)

# Saving the processed data to an absolute path
output_path = os.path.join(BASE_DIR, "data/processed_data.csv")
final_df.to_csv(output_path, index=False)
print(f"✅ Success! Data ready for training at: {output_path}")