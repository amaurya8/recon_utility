import pandas as pd

def highlight_diff(self, row):
    """Highlights mismatched cells."""
    styles = [''] * len(row)
    start_idx = len(self.config['comparison_keys'])

    for i in range(start_idx, len(row) - 1, 2):
        val1 = row.iloc[i]
        val2 = row.iloc[i + 1]

        # Handle NaN-safe comparison
        if pd.isna(val1) and pd.isna(val2):
            continue
        if not pd.isna(val1) and not pd.isna(val2) and val1 != val2:
            styles[i] = 'background-color: #FF6347'
            styles[i + 1] = 'background-color: #FF6347'
        elif pd.isna(val1) != pd.isna(val2):  # One is NaN, other is not
            styles[i] = 'background-color: #FF6347'
            styles[i + 1] = 'background-color: #FF6347'

    return styles