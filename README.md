<img width="1904" height="909" alt="image" src="https://github.com/user-attachments/assets/b9f867d6-db9c-4b64-8f49-76b640c32c76" />

# Hypertension Risk & Patient Trend Dashboard

This project is an end-to-end pipeline that takes the UCI Heart Disease dataset and turns it into a longitudinal monitoring tool. Since clinical history is hard to find for privacy reasons, I built a simulation engine to generate 6 months of visit data for each patient to show how blood pressure trends would look in a real clinic.

# What this does

ETL Pipeline: Fetches raw data from UCI, cleans it (handling missing values/types), and simulates a 6-month history.

Database: Moves processed data into a relational SQLite database split into patients and vitals tables.

Analysis: Uses SQL window functions to track BP percentage changes over time.

UI: A Streamlit dashboard with Plotly charts to visualize "Warning" (140mmHg) and "Crisis" (180mmHg) thresholds.

# The Logic
The simulation isn't just random numbers. If a patient was marked as high-risk in the original dataset, they have a 70% chance of their blood pressure trending upward each month. I also added a 5% random spike (180-205 mmHg) to simulate hypertensive crises for the dashboard’s alert system.

# Setup

    git clone https://github.com/cayla-hhh/End-to-End-Hypertension-Pipeline.git

    cd End-to-End-Hypertension-Pipeline
    
#### Environment & Dependencies

    python -m venv venv
    
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    pip install -r requirements.txt
    
#### Build the Database:

Run these in order to build the database:

    python scripts/extract.py

    python scripts/transform.py

    python scripts/load_sql.py

#### Launch Dashboard:

    streamlit run app/app.py

# File Structure

scripts/extract.py: Pulls the .data file from UCI.

scripts/transform.py: Cleans the data and runs the NumPy simulation.

scripts/load_sql.py: Normalizes the data and handles the SQLite upload.

app/app.py: The dashboard UI and Plotly logic.

hypertension_data.db: The generated relational database.
