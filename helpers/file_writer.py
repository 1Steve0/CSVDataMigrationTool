import os
import pandas as pd

def save_transformed(df: pd.DataFrame, adapter_name: str) -> str:
    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", f"{adapter_name}_transformed.csv")
    df.to_csv(output_path, index=False)
    return output_path