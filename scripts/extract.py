import requests
import os

DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEST_PATH = os.path.join(BASE_DIR, "..", "data", "raw", "heart_data_raw.csv")

def extract_data():
    print("Starting extraction...")
    
    try:
        response = requests.get(DATA_URL)
        response.raise_for_status()
        
        
        with open(DEST_PATH, "wb") as f:
            f.write(response.content)
            
        print(f"Success! Raw data saved to: {DEST_PATH}")
        
    except Exception as e:
        print(f"Extraction failed: {e}")


if __name__ == "__main__":
    extract_data()