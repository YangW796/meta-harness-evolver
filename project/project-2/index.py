import pandas as pd
def compute_x(df: pd.DataFrame) -> pd.Series:
    return df["iptm"] - 0.1 * df["DDG"] - 0.01 * df["SAP Score"] - 0.1 * df["FV Charge"].abs()
import numpy as np
import pandas as pd
def compute_x0(df: pd.DataFrame) -> pd.Series:
    x1 = df["iptm"].values
    x2 = df["DDG"].values
    x3 = df["SAP Score"].values
    x4 = df["FV Charge"].values

    # ===== 数值稳定函数 =====
    def safe_log(x):
        return np.log(np.clip(x, 1e-8, None))

    def safe_exp(x):
        return np.exp(np.clip(x, -20, 20))

    def safe_cosh(x):
        return np.cosh(np.clip(x, -10, 10))

    # ===== 非线性组合 =====
    term1 = safe_exp(
        np.sin(x1 * x2) + np.cos(x3**2 - x4)
    ) * np.tanh(
        x1**2 * x3 - (x2 * x4) / (1 + x1**2 + x4**2)
    )

    term2 = safe_log(
        1 + x1**2 + x2**2 + x3**2 + x4**2 +
        np.abs(np.sin(x1 * x4 - x2 * x3))
    ) / (1 + (x1 - x2 * x3)**2)

    term3 = np.sin(
        safe_exp(np.cos(x1 + x3)) + x2**3 / (1 + x4**2)
    ) * np.cos(
        safe_log(1 + x1**2 * x2**2 + x3**2)
    )

    term4 = np.sinh(
        np.sin(x1 * x2 * x3)
    ) / (1 + safe_cosh(x4 - x1 * x2))

    term5 = np.arctan(
        (x1 - x3)**3 +
        (x2 + x4)**2 +
        np.sin(x1 * x2 - x3 * x4)
    )

    y = term1 + term2 + term3 + term4 + term5

    # ===== 标准化（推荐保留）=====
    y = (y - np.mean(y)) / (np.std(y) + 1e-8)

    return pd.Series(y, index=df.index)