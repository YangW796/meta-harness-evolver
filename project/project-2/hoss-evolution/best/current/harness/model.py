from __future__ import annotations

import numpy as np


class BaseModel:
    """
    A minimal model interface.

    NOTE:
    - This model can be a deep learning model, a machine learning model,
      a mathematical model, or any scientific simulation model.
    - You are free to design training logic (or no training at all).
    - The model should output a single scalar value for each input sample.
    """

    def __init__(self, input_dim: int):
        self.input_dim = input_dim

    def fit(self, X: np.ndarray, y: np.ndarray):
        """
        Train the model.

        You can:
        - implement training
        - or skip training (e.g., rule-based / analytical model)
        """
        pass

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict output values.

        Must return shape (N,) or (N, 1).
        """
        # Example dummy implementation
        return np.zeros(len(X))


def train_model(
    X_train: np.ndarray,
    y_train: np.ndarray,
    input_dim: int,
    device: str,
    seed: int,
) -> object:
    """
    Train and return a model.

    NOTE:
    - The model can be:
        * deep learning model (PyTorch, TensorFlow, etc.)
        * classical ML model (sklearn, xgboost, etc.)
        * mathematical/scientific model
    - Training is optional and fully customizable.
    """

    np.random.seed(int(seed))

    model = BaseModel(input_dim=input_dim)

    # User-defined training logic
    model.fit(X_train, y_train)

    return model


def predict_model(model: object, X: np.ndarray, device: str) -> np.ndarray:
    """
    Run prediction.

    NOTE:
    - The model must output a single value per sample.
    - Device argument is kept for compatibility but may be unused.
    """

    if not hasattr(model, "predict"):
        raise TypeError("model must implement a predict() method")

    pred = model.predict(X)
    return np.asarray(pred)


def save_model(model: object, path: str) -> None:
    """
    Save the model.

    NOTE:
    - You can use:
        * pickle
        * joblib
        * torch.save
        * custom format
    """

    import pickle

    with open(path, "wb") as f:
        pickle.dump(model, f)


def load_model(path: str, input_dim: int, device: str) -> object:
    """
    Load the model.

    NOTE:
    - Must match the save_model format.
    - input_dim/device are kept for compatibility but may not be used.
    """

    import pickle

    with open(path, "rb") as f:
        model = pickle.load(f)

    return model