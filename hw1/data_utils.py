def process_sensor_data(raw_data, **config):
    """
    Processes sensor data with optional configurations.

    Options:
    remove_outliers=True
    smooth=True
    scale="normalize" or "standardize"
    """

    data = raw_data[:]

    if config.get("remove_outliers"):
        mean = sum(data) / len(data)
        variance = sum((x - mean) ** 2 for x in data) / len(data)
        std = variance ** 0.5
        data = [x for x in data if abs(x - mean) <= 3 * std]

    if config.get("smooth") and len(data) >= 3:
        smoothed = []
        for i in range(1, len(data) - 1):
            smoothed.append((data[i - 1] + data[i] + data[i + 1]) / 3)
        data = smoothed

    scale = config.get("scale")
    if scale == "normalize":
        mn, mx = min(data), max(data)
        data = [(x - mn) / (mx - mn) for x in data]
    elif scale == "standardize":
        mean = sum(data) / len(data)
        variance = sum((x - mean) ** 2 for x in data) / len(data)
        std = variance ** 0.5
        data = [(x - mean) / std for x in data]

    return data
