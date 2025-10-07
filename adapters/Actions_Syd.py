# adapters/Actions_Sydneywater.py

import os
import pandas as pd
from helpers.file_writer import save_transformed

column_map = {
    "Id": "Legacy Id (Admin Only)",
    "Address": "Address",
    "Auto Geocode": "Auto Geocode",
    "Country": "Country",
    "Distribution Lists": "Distribution Lists",
    "Location": "Location",
    "Notes": "Notes",
    "Post Code": "Post Code",
    "Property Groups": "Property Groups",
    "Property Name": "Property Name",
    "Property Number": "Property Number",
    "Reference": "Reference",
    "State": "State",
    "Suburb": "Suburb"
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



