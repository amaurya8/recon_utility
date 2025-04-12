import pandas as pd
import numpy as np

def highlight_diff(self, row):
    styles = [''] * len(row)
    start_idx = len(self.config['comparison_keys'])

    for i in range(start_idx, len(row) - 1, 2):
        val1 = row.iloc[i]
        val2 = row.iloc[i + 1]

        if pd.isna(val1) and pd.isna(val2):
            continue
        elif pd.isna(val1) or pd.isna(val2):
            mismatch = True
        elif isinstance(val1, (int, float, np.number)) and isinstance(val2, (int, float, np.number)):
            mismatch = not np.isclose(val1, val2, equal_nan=True)
        else:
            mismatch = str(val1) != str(val2)

        if mismatch:
            styles[i] = 'background-color: #FF6347'
            styles[i + 1] = 'background-color: #FF6347'

    return styles



import numpy as np

def standardize_nulls(df):
    return df.replace(['', ' ', None], np.nan)