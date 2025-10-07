# adapters/Organisations_sydneywater.py

import os
import pandas as pd
from helpers.file_writer import save_transformed

column_map = {
    "Id": "Legacy Id (Admin Only)",
    "Address": "Address",
    "Country": "Country",
    "Email": "Email",
    "Location": "Location",
    "Name": "Name",
    "Phone": "Phone",
    "Post Code": "Post Code",
    "Primary Contact": "Primary Contact",
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



