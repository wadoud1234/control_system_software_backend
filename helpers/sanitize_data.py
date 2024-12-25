import math

import numpy as np


def sanitize_data(data):
    """
    Recursively sanitize the data to replace Infinity, -Infinity, and NaN.
    """
    if isinstance(data, dict):
        return {key: sanitize_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [sanitize_data(item) for item in data]
    elif isinstance(data, (float, np.float64, np.float32)):
        if math.isinf(data):
            return "Infinity" if data > 0 else "-Infinity"
        elif math.isnan(data):
            return "NaN"
    return data