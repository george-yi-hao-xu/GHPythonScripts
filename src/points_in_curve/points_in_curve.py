"""
Inputs:
    points: Point list to test
    curve: Closed planar curve

Outputs:
    A: Points inside curve
    B: Points outside curve
    C: Points not on curve plane
    message: Status message
"""

import Rhino.Geometry as rg
from typing import cast

# Grasshopper supplies these names from the component inputs at runtime.
# This `cast` is just to satisfy the type checker and has no effect at runtime.
points = cast(list[rg.Point3d], globals()["points"])
curve = cast(rg.Curve, globals()["curve"])


inside_pts = []
outside_pts = []
invalid_pts = []

tol = 0.001

# Try getting plane from curve
success, plane = curve.TryGetPlane()

# Guard clause
if not success:
    A = inside_pts
    B = outside_pts
    C = invalid_pts
    message = "Input curve is not planar."
else:

    for pt in points:

        # Check if point is near curve plane
        if abs(plane.DistanceTo(pt)) > tol:
            invalid_pts.append(pt)
            continue

        result = curve.Contains(pt, plane, tol)

        if result == rg.PointContainment.Inside:
            inside_pts.append(pt)
        else:
            outside_pts.append(pt)

    A = inside_pts
    B = outside_pts
    C = invalid_pts

    message = (
        "Success.\n"
        "Inside: {}\n"
        "Outside: {}\n"
        "Off plane: {}"
    ).format(
        len(inside_pts),
        len(outside_pts),
        len(invalid_pts)
    )
