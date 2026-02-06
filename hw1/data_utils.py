def process_sensor_data(raw_data, **config):
    """
    Processes sensor data with optional configurations (using **kwargs).
    Config options (all optional):
    - remove_outliers=True : discard readings that are > 3 standard deviations from mean
    - smooth=True : apply a 3-point moving average
    - scale="normalize" : scale values to range 0 to 1
    - scale="standardize" : convert to z-scores (mean 0, std 1)
    - Unknown options: ignore (do nothing)
    """

    # slicing
    data = raw_data[:]

    # remove_outliers option
    # -----------------------------
    if config.get("remove_outliers") == True:
        # mean = sum / count
        mean = sum(data) / len(data)

        #using len(data)
        variance = 0.0
        for x in data:
            variance += (x - mean) ** 2
        variance = variance / len(data)

        # standard deviation
        std = variance ** 0.5

        # filter out values too far from mean
        filtered = []
        for x in data:
            if abs(x - mean) <= 3 * std:
                filtered.append(x)

        # replace data with the filtered list
        data = filtered

    # smooth option
    # moving average needs at least 3 items to have a middle point
    if config.get("smooth") == True and len(data) >= 3:
        # only for the middle indices (1 to len-2)
        smoothed = []

        # start at 1 and stop at len(data)-1
        for i in range(1, len(data) - 1):
            avg = (data[i - 1] + data[i] + data[i + 1]) / 3
            smoothed.append(avg)

        #update  to smoothed list
        data = smoothed

    # scale option
    scale_mode = config.get("scale")  #"normalize", "standardize", or None

    #(x - min) / (max - min)
    if scale_mode == "normalize":
        mn = min(data)
        mx = max(data)

        #prevent division by zero if mn == mx
        if mx == mn:
            data = [0.0 for x in data] # if all values are same, normalized values would be all 0.0
        else:
            normalized = []
            for x in data:
                normalized.append((x - mn) / (mx - mn))
            data = normalized

    #  (x - mean) / std
    elif scale_mode == "standardize":
        mean = sum(data) / len(data)

        variance = 0.0
        for x in data:
            variance += (x - mean) ** 2
        variance = variance / len(data)

        std = variance ** 0.5

        # prevent division by zero if std == 0
        if std == 0:
            data = [0.0 for x in data]
        else:
            standardized = []
            for x in data:
                standardized.append((x - mean) / std)
            data = standardized

    # ignore (do nothing)
    else:
        pass

    return data
