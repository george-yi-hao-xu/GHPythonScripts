DEFAULT_CONFIG = {
    "min_area": 1.0,
    "max_depth": 8,
    "seed": 1,
    "crack_variation": 0.25,
    "tol": None,
}

CONFIG_TYPES = {
    "min_area": float,
    "max_depth": int,
    "seed": int,
    "crack_variation": float,
    "tol": float,
}


def parse_config_value(key, value):
    value = str(value).strip()

    if key == "tol" and value.lower() in ("", "none", "null"):
        return None

    return CONFIG_TYPES[key](value)


def parse_config_text(text):
    values = {}
    errors = []

    if not text:
        return values, errors

    for line_number, raw_line in enumerate(str(text).splitlines(), 1):
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        if "=" in line:
            key, value = line.split("=", 1)
        elif ":" in line:
            key, value = line.split(":", 1)
        else:
            errors.append("Line {} has no '=' or ':'.".format(line_number))
            continue

        key = key.strip()
        if key not in CONFIG_TYPES:
            errors.append("Line {} has unknown key '{}'.".format(line_number, key))
            continue

        try:
            values[key] = parse_config_value(key, value)
        except ValueError:
            errors.append(
                "Line {} has invalid value for '{}'.".format(line_number, key)
            )

    return values, errors


def read_config_file(path):
    if not path:
        return "", None

    try:
        with open(str(path), "r") as config_file:
            return config_file.read(), None
    except Exception as error:
        return "", "Could not read config_path: {}".format(error)


def component_config(global_values):
    config = DEFAULT_CONFIG.copy()
    errors = []

    file_text, file_error = read_config_file(global_values.get("config_path", None))
    if file_error:
        errors.append(file_error)

    for text in (
        file_text,
        global_values.get("config", None),
        global_values.get("config_text", None),
    ):
        parsed, parse_errors = parse_config_text(text)
        config.update(parsed)
        errors.extend(parse_errors)

    for key in DEFAULT_CONFIG:
        if key not in global_values or global_values[key] is None:
            continue

        try:
            config[key] = parse_config_value(key, global_values[key])
        except ValueError:
            errors.append("Input '{}' has invalid value.".format(key))

    return config, errors
