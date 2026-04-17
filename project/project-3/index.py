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
    return compute_x(df)
