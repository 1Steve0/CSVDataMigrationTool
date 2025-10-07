# adapters/Events_SydneyWater.py

import os
import pandas as pd
from helpers.file_writer import save_transformed

column_map = {
    "Id": "Legacy Id (Admin Only)",
    "Address": "Address",
    "Auto Geocode": "Auto Geocode",
    "Country": "Country",
    "End Date": "End Date",
    "Event Type": "Event Type",
    "Issues": "Issues",
    "Location": "Location",
    "Post Code": "Post Code",
    "Sentiment": "Sentiment",
    "Stakeholder Comments": "Stakeholder Comments",
    "Start Date": "Start Date",
    "State": "State",
    "Suburb": "Suburb",
    "Summary": "Summary",
    "Team Response": "Team Response"
}

def transform(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [col.strip() for col in df.columns]
    mapped_columns = {src: tgt for src, tgt in column_map.items() if src in df.columns}
    df = df[list(mapped_columns.keys())].rename(columns=mapped_columns)

    # if "Email" in df.columns:
    #     df["Email"] = df["Email"].astype(str).str.strip().str.lower()

    # if "First Name" in df.columns and "Last Name" in df.columns:
    #     df["Full Name"] = df["First Name"].fillna("") + " " + df["Last Name"].fillna("")

    return df

def save_transformed(df: pd.DataFrame, adapter_name: str) -> str:
    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", f"{adapter_name}_transformed.csv")
    df.to_csv(output_path, index=False)
    return output_path
