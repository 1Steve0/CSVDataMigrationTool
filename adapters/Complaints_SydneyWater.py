# adapters/Complaints_sydneywater.py

import os
import pandas as pd
from helpers.file_writer import save_transformed

column_map = {
    "Id": "Legacy Id (Admin Only)",
    "Action Taken": "Action Taken",
    "Address": "Address",
    "Complaint Channel": "Complaint Channel",
    "Country": "Country",
    "Date Closed": "Date Closed",
    "Date Received": "Date Received",
    "Details of Complaint": "Details of Complaint",
    "Expected Escalation": "Expected Escalation",
    "Follow Up": "Follow Up",
    "Follow Up Sentiment": "Follow Up Sentiment",
    "Initial response date": "Initial response date",
    "Location": "Location",
    "Post Code": "Post Code",
    "Sentiment": "Sentiment",
    "State": "State",
    "Suburb": "Suburb",
    "Type of Complaint": "Type of Complaint"
}

def transform(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [col.strip() for col in df.columns]
    mapped_columns = {src: tgt for src, tgt in column_map.items() if src in df.columns}
    df = df[list(mapped_columns.keys())].rename(columns=mapped_columns)

    if "Email" in df.columns:
        df["Email"] = df["Email"].astype(str).str.strip().str.lower()

    # if "First Name" in df.columns and "Last Name" in df.columns:
    #     df["Full Name"] = df["First Name"].fillna("") + " " + df["Last Name"].fillna("")

    return df



