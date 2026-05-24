import Rhino.Geometry as rg


# Normalize accepted Grasshopper geometry inputs into one planar Brep.
def coerce_planar_brep(geometry, tolerance):
    if isinstance(geometry, rg.Brep):
        brep = geometry.DuplicateBrep()
    elif isinstance(geometry, rg.BrepFace):
        brep = geometry.DuplicateFace(False)
    elif isinstance(geometry, rg.Surface):
        brep = geometry.ToBrep()
    elif isinstance(geometry, rg.Curve):
        if not geometry.IsClosed:
            return None, "Input curve is not closed."

        breps = rg.Brep.CreatePlanarBreps(geometry, tolerance)
        if not breps or len(breps) == 0:
            return None, "Input curve is not planar or cannot make a surface."

        brep = breps[0]
    else:
        return None, "Input must be a planar Surface, Brep, BrepFace, or closed Curve."

    if not brep or brep.Faces.Count == 0:
        return None, "Could not convert input to a Brep."

    face = brep.Faces[0]
    try:
        success, plane = face.TryGetPlane(tolerance)
    except TypeError:
        success, plane = face.TryGetPlane()

    if not success:
        return None, "Input Brep face is not planar."

    return brep, None


def brep_area(brep):
    props = rg.AreaMassProperties.Compute(brep)
    if not props:
        return 0.0

    return props.Area


def normalized_point(curve, value):
    success, parameter = curve.NormalizedLengthParameter(value)
    if not success:
        parameter = curve.Domain.ParameterAt(value)

    return curve.PointAt(parameter)


# Return the outer boundary edge curves with loop order and length, so the
# crack logic can find long sides to connect with a splitting line.
def outer_boundary_segments(brep):
    face = brep.Faces[0]
    outer_loop = None

    for loop in face.Loops:
        if loop.LoopType == rg.BrepLoopType.Outer:
            outer_loop = loop
            break

    if outer_loop is None:
        return []

    segments = []
    for index, trim in enumerate(outer_loop.Trims):
        edge = trim.Edge
        if edge is None:
            continue

        curve = edge.DuplicateCurve()
        if curve is None:
            continue

        length = curve.GetLength()
        if length <= 0.0:
            continue

        segments.append({
            "index": index,
            "curve": curve,
            "length": length,
        })

    return segments
