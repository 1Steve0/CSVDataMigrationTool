# adapters/stakeholders_sydneywater.py

import os
import pandas as pd
from helpers.file_writer import save_transformed

column_map = {
    "Id": "Legacy Id (Admin Only)",
    "Title": "Title",
    "First Name": "First Name",
    "Last Name": "Last Name",
    "Suffix": "Suffix",
    "Role": "Role",
    "Organisation": "Organisation",
    "BH Phone": "BH Phone",
    "AH Phone": "AH Phone",
    "Mobile": "Mobile",
    "Fax": "Fax",
    "Email": "Email",
    "Web Address": "Web Address",
    "Notes": "Notes",
    "Stakeholder Groups": "Stakeholder Segments",
    "Stakeholder Distribution Lists": "Distribution Lists",
    "Address": "Address",
    "Post Code": "Post Code",
    "Suburb": "Suburb",
    "State": "State",
    "Country": "Country",
    "Location": "Location",
    "Privacy": "Privacy",
    "Auto Geocode": "Auto Geocode"
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



