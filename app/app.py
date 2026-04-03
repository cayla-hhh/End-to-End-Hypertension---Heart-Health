import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "hypertension_data.db")
engine = create_engine(f"sqlite:///{DB_PATH}")

st.set_page_config(page_title="Hypertension Risk Tracker", layout="wide")

st.title("Patient Hypertension Risk Dashboard")
st.markdown("monitoring longitudinal trends and urgent clinical alerts.")

st.sidebar.header("System Navigation")

alert_query = """
SELECT p.patient_id, v.trestbps, v.visit_date
FROM patients p
JOIN vitals v ON p.patient_id = v.patient_id
WHERE v.is_crisis = 1
ORDER BY v.visit_date DESC;
"""
alerts_df = pd.read_sql(alert_query, engine)

with st.sidebar:
    st.error("URGENT ALERTS")
    if not alerts_df.empty:
        for _, row in alerts_df.iterrows():
            st.warning(
                f"**Patient {int(row['patient_id'])}**\n"
                f"BP: {row['trestbps']} mmHg\n"
                f"Date: {row['visit_date']}"
            )
    else:
        st.success("No active hypertensive crises.")