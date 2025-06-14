# scripts/utils.py

import pandas as pd
import json
from typing import Union
from pathlib import Path

def save_dataframe_json(df: pd.DataFrame, output_path: Union[str, Path]) -> None:
    """Save a DataFrame to JSON.

    Args:
        df (pd.DataFrame): Data to save.
        output_path (str | Path): Destination path for the JSON file.
    """
    output_path = Path(output_path)
    df.to_json(output_path, orient='records', indent=4)
    print(f"💾 Saved JSON to {output_path}")

def save_dataframe_excel(df: pd.DataFrame, output_path: Union[str, Path], highlight_column: str = 'flagged_as_unreliable') -> None:
    """Save DataFrame to Excel with optional row highlighting.

    Args:
        df (pd.DataFrame): Data to save.
        output_path (str | Path): Destination path for the Excel file.
        highlight_column (str): Boolean column used for conditional highlighting.
    """
    output_path = Path(output_path)

    def highlight_unreliable(s):
        return ['background-color: #FFB3BA' if v else '' for v in s]

    if highlight_column in df.columns:
        styled = df.style.apply(highlight_unreliable, subset=[highlight_column])
    else:
        styled = df.style

    styled.to_excel(output_path, index=False, engine='openpyxl')
    print(f"📁 Saved Excel to {output_path}")
