from .cracking import crack_brep
from .config import component_config
from .geometry import brep_area, coerce_planar_brep
from .utils import get_tolerance


# Grasshopper supplies these names from the component inputs at runtime.
surface = globals()["surface"]
config, config_errors = component_config(globals())


tolerance = get_tolerance(config["tol"])
minimum_area = max(float(config["min_area"]), tolerance)
depth_limit = max(int(config["max_depth"]), 0)

input_brep, error = coerce_planar_brep(surface, tolerance)

if config_errors:
    A = []
    B = []
    C = []
    message = "Config error.\n" + "\n".join(config_errors)
elif error:
    A = []
    B = []
    C = []
    message = error
else:
    cracked_surfaces, crack_curves, split_attempts = crack_brep(
        input_brep,
        minimum_area,
        depth_limit,
        config["crack_variation"],
        config["seed"],
        tolerance,
    )
    areas = [brep_area(piece) for piece in cracked_surfaces]

    A = cracked_surfaces
    B = crack_curves
    C = areas
    message = (
        "Success.\n"
        "Pieces: {}\n"
        "Cracks: {}\n"
        "Split attempts: {}\n"
        "Min area: {:.3f}"
    ).format(
        len(cracked_surfaces),
        len(crack_curves),
        split_attempts,
        minimum_area,
    )
