from __future__ import annotations

import numpy as np

try:
    import pandas as pd
except ModuleNotFoundError:
    pd = None


def _as_float_array(values: object, n: int | None = None) -> np.ndarray:
    if isinstance(values, np.ndarray):
        out = values.astype(np.float64, copy=False).reshape(-1)
    else:
        out = np.asarray(list(values), dtype=np.float64).reshape(-1)
    if n is not None and len(out) != n:
        raise ValueError(f"Column length mismatch: expected {n}, got {len(out)}")
    out[~np.isfinite(out)] = 0.0
    return out


def compute_x(df: object) -> np.ndarray:
    if pd is not None and hasattr(pd, "DataFrame") and isinstance(df, pd.DataFrame):
        iptm = _as_float_array(df["iptm"].to_numpy(), n=len(df))
        ddg = _as_float_array(df["DDG"].to_numpy(), n=len(df))
        sap = _as_float_array(df["SAP Score"].to_numpy(), n=len(df))
        fv = _as_float_array(df["FV Charge"].to_numpy(), n=len(df))
        return iptm - 0.1 * ddg - 0.01 * sap - 0.1 * np.abs(fv)

    if isinstance(df, dict):
        iptm = _as_float_array(df["iptm"])
        n = int(len(iptm))
        ddg = _as_float_array(df["DDG"], n=n)
        sap = _as_float_array(df["SAP Score"], n=n)
        fv = _as_float_array(df["FV Charge"], n=n)
        return iptm - 0.1 * ddg - 0.01 * sap - 0.1 * np.abs(fv)

    if isinstance(df, list):
        iptm = _as_float_array([row["iptm"] for row in df])
        n = int(len(iptm))
        ddg = _as_float_array([row["DDG"] for row in df], n=n)
        sap = _as_float_array([row["SAP Score"] for row in df], n=n)
        fv = _as_float_array([row["FV Charge"] for row in df], n=n)
        return iptm - 0.1 * ddg - 0.01 * sap - 0.1 * np.abs(fv)

    raise TypeError("compute_x expects a pandas.DataFrame, a dict-of-columns, or a list of row dicts")


def compute_x0(df: object) -> np.ndarray:
    def _compute_from_arrays(x1: np.ndarray, x2: np.ndarray, x3: np.ndarray, x4: np.ndarray) -> np.ndarray:
        def safe_log(x: np.ndarray) -> np.ndarray:
            return np.log(np.clip(x, 1e-8, None))

        def safe_exp(x: np.ndarray) -> np.ndarray:
            return np.exp(np.clip(x, -20, 20))

        def safe_cosh(x: np.ndarray) -> np.ndarray:
            return np.cosh(np.clip(x, -10, 10))

        term1 = safe_exp(np.sin(x1 * x2) + np.cos(x3**2 - x4)) * np.tanh(
            x1**2 * x3 - (x2 * x4) / (1 + x1**2 + x4**2)
        )
        term2 = safe_log(
            1 + x1**2 + x2**2 + x3**2 + x4**2 + np.abs(np.sin(x1 * x4 - x2 * x3))
        ) / (1 + (x1 - x2 * x3) ** 2)
        term3 = np.sin(safe_exp(np.cos(x1 + x3)) + x2**3 / (1 + x4**2)) * np.cos(
            safe_log(1 + x1**2 * x2**2 + x3**2)
        )
        term4 = np.sinh(np.sin(x1 * x2 * x3)) / (1 + safe_cosh(x4 - x1 * x2))
        term5 = np.arctan((x1 - x3) ** 3 + (x2 + x4) ** 2 + np.sin(x1 * x2 - x3 * x4))
        y = term1 + term2 + term3 + term4 + term5
        y = (y - np.mean(y)) / (np.std(y) + 1e-8)
        return y.astype(np.float64, copy=False)

    if pd is not None and hasattr(pd, "DataFrame") and isinstance(df, pd.DataFrame):
        x1 = _as_float_array(df["iptm"].to_numpy(), n=len(df))
        x2 = _as_float_array(df["DDG"].to_numpy(), n=len(df))
        x3 = _as_float_array(df["SAP Score"].to_numpy(), n=len(df))
        x4 = _as_float_array(df["FV Charge"].to_numpy(), n=len(df))
        return _compute_from_arrays(x1, x2, x3, x4)

    if isinstance(df, dict):
        x1 = _as_float_array(df["iptm"])
        n = int(len(x1))
        x2 = _as_float_array(df["DDG"], n=n)
        x3 = _as_float_array(df["SAP Score"], n=n)
        x4 = _as_float_array(df["FV Charge"], n=n)
        return _compute_from_arrays(x1, x2, x3, x4)

    if isinstance(df, list):
        x1 = _as_float_array([row["iptm"] for row in df])
        n = int(len(x1))
        x2 = _as_float_array([row["DDG"] for row in df], n=n)
        x3 = _as_float_array([row["SAP Score"] for row in df], n=n)
        x4 = _as_float_array([row["FV Charge"] for row in df], n=n)
        return _compute_from_arrays(x1, x2, x3, x4)

    raise TypeError("compute_x0 expects a pandas.DataFrame, a dict-of-columns, or a list of row dicts")
