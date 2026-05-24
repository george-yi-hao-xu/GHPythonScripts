import Rhino


def clamp(value, low, high):
    return max(low, min(high, value))


def get_tolerance(tolerance_override):
    if tolerance_override is not None:
        return float(tolerance_override)

    doc = Rhino.RhinoDoc.ActiveDoc
    if doc:
        return doc.ModelAbsoluteTolerance

    return 0.001

