import numpy as np


def converter_para_json_serializavel(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: converter_para_json_serializavel(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [converter_para_json_serializavel(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(converter_para_json_serializavel(item) for item in obj)
    else:
        return obj

