import pandas as pd
from sqlalchemy import create_engine
import os

current_dir = os.path.dirname(os.path.abspath(__file__))


project_root = os.path.abspath(os.path.join(current_dir, ".."))

DB_PATH = os.path.join(project_root, "hypertension_data.db")


engine = create_engine(f"sqlite:///{DB_PATH}")

query = """
WITH RankedVitals AS (
    SELECT
        patient_id,
        trestbps,
        visit_date,
        ROW_NUMBER() OVER(PARTITION BY patient_id ORDER BY visit_date ASC) as first_visit,
        ROW_NUMBER() OVER(PARTITION BY patient_id ORDER BY visit_date DESC) as last_visit
    FROM vitals
)
SELECT
    p.patient_id,
    p.age,
    v1.trestbps AS start_bp,
    v2.trestbps AS latest_bp,
    ROUND(((v2.trestbps - v1.trestbps) / v1.trestbps) * 100, 2) AS pct_change
FROM patients p
JOIN RankedVitals v1 ON p.patient_id = v1.patient_id AND v1.first_visit = 1
JOIN RankedVitals v2 ON p.patient_id = v2.patient_id AND v2.last_visit = 1
WHERE pct_change > 10
ORDER BY pct_change DESC;
"""

df_trends = pd.read_sql(query, engine)
print("Patients with >10% BP Increase:")
print(df_trends.head())