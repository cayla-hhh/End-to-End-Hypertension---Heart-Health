import pandas as pd
from sqlalchemy import create_engine
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(BASE_DIR, '..', 'data', 'processed', 'patient_history.csv')

engine = create_engine("sqlite:///../hypertension_data.db")

def load_to_sqlite():
    df = pd.read_csv(INPUT_PATH)

    patients_df = df[['patient_id', 'age', 'sex', 'target']].drop_duplicates()

    vitals_df = df[['patient_id', 'visit_date', 'trestbps', 'is_crisis']]

    patients_df.to_sql("patients", engine, if_exists='replace', index=False)
    vitals_df.to_sql("vitals", engine, if_exists='replace', index=False)
    
if __name__ == "__main__":
    load_to_sqlite()