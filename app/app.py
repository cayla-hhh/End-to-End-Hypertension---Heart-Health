import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
import plotly.graph_objects as go

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "hypertension_data.db")

absolute_db_path = os.path.abspath(DB_PATH)
engine = create_engine(f"sqlite:///{absolute_db_path}")

st.set_page_config(page_title="Hypertension Risk Tracker", layout="wide")

st.title("Patient Hypertension Risk Dashboard")
st.markdown("Monitoring longitudinal trends and urgent clinical alerts.")

col1, col2, col3 = st.columns(3)

total_patients = pd.read_sql("SELECT COUNT(*) FROM patients", engine).iloc[0, 0]

high_risk_query = "SELECT COUNT(*) FROM patients WHERE target > 0"
high_risk_count = pd.read_sql(high_risk_query, engine).iloc[0, 0]

avg_bp_query = """
SELECT AVG(trestbps) FROM vitals
WHERE (patient_id, visit_date) IN (
    SELECT patient_id, MAX(visit_date) FROM vitals GROUP BY patient_id
    )
"""
avg_bp = pd.read_sql(avg_bp_query, engine).iloc[0, 0]

with col1:
    st.metric("Total Patients", total_patients)
with col2:
    st.metric("High-Risk Patients", high_risk_count)
with col3:
    st.metric("Avg. Systolic BP", f"{avg_bp:.1f} mmHg")

st.header("Individual Patient Analysis")

patient_ids = pd.read_sql("SELECT patient_id FROM patients", engine)['patient_id'].tolist()
selected_id = st.selectbox("Select Patient ID", patient_ids)

if selected_id:
    history_query = f"SELECT visit_date, trestbps FROM vitals WHERE patient_id = {selected_id} ORDER BY visit_date"
    df_patient = pd.read_sql(history_query, engine)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_patient['visit_date'],
        y=df_patient['trestbps'],
        mode='lines+markers',
        name='Systolic BP',
        line=dict(color="#1f77b4", width=3),
    ))

    # Line at 180 Danger Zone
    fig.add_trace(go.Scatter(
        x=df_patient['visit_date'],
        y=[180] * len(df_patient),
        mode='lines',
        name='Crisis Threshold (180)',
        line=dict(color='red', width=2, dash='dash'),
    ))

    # Line at 140 Warning Zone
    fig.add_trace(go.Scatter(
        x=df_patient['visit_date'],
        y=[140] * len(df_patient),
        mode='lines',
        name='Warning (140)',
        line=dict(color='orange', width=2, dash='dot'),
    ))
    fig.update_layout(
        title=f"Blood Pressure Trend for Patient {selected_id}",
        xaxis_title="visit Date",
        yaxis_title="BP (mmHg)",
        yaxis=dict(range=[100, 210]),
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader(f"Visit Logs for Patient {selected_id}")
    st.dataframe(df_patient.sort_values(by="visit_date", ascending=False), use_container_width=True)

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