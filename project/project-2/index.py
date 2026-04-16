import pandas as pd
def compute_x(df: pd.DataFrame) -> pd.Series:
    return df["iptm"] - 0.1 * df["DDG"] - 0.01 * df["SAP Score"] - 0.1 * df["FV Charge"].abs()