import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta


columns = [
    "age", "sex", "cp", "trestbps", "chol", "fbs",
    "restecg", "thalach", "exang", "oldpeak",
    "slope", "ca", "thal", "target"
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(BASE_DIR, "..", "data", "raw", "heart_data_raw.csv")

def transform_data():
    df = pd.read_csv(INPUT_PATH, names=columns)
    df = df.replace('?', pd.NA)

    df = df.dropna()

    numeric_cols = ["age", "trestbps", "chol", "thalach", "ca", "thal"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)

    df['sex'] = df['sex'].map({1: 'Male', 0: 'Female'})

    print(df[['age', 'sex', 'trestbps']].head())

    return df

def simulate_history(df):
    history_records = []
    df = df.reset_index().rename(columns={'index':'patient_id'})

    for _, patient in df.iterrows():
        base_bp = patient['trestbps']

        for month in range(6):
            if patient['target'] > 0 and np.random.random() < 0.7:
                variation = np.random.uniform(1.02, 1.05)
            else:
                variation = np.random.uniform(0.98, 1.02)

            new_bp = base_bp * (variation ** month)
            
            is_crisis = False
            if patient['target'] > 0 and np.random.random() < 0.05:
                new_bp = np.random.uniform(180, 205)
                is_crisis = True

            visit_date = datetime(2024, 1, 1) + timedelta(days=30 * month)

            record = patient.to_dict()
            record['trestbps'] = round(new_bp, 1)
            record['visit_date'] = visit_date
            record['visit_number'] = month + 1
            record['is_crisis'] = is_crisis
            
            history_records.append(record)

    return pd.DataFrame(history_records)

if __name__ == "__main__":
    clean_df = transform_data()

    final_history_df = simulate_history(clean_df)
    processed_path = os.path.join(BASE_DIR, "..", "data", "processed","patient_history.csv")
    final_history_df.to_csv(processed_path, index=False)

    print(f"Processed {len(final_history_df)} records to {processed_path}")