import random

import Rhino.Geometry as rg
from System.Collections.Generic import List

from .geometry import brep_area, normalized_point, outer_boundary_segments
from .utils import clamp


def candidate_side_pairs(segments):
    count = len(segments)
    if count < 2:
        return []

    pairs = []
    for i in range(count):
        for j in range(i + 1, count):
            loop_gap = abs(segments[i]["index"] - segments[j]["index"])
            adjacent = loop_gap == 1 or loop_gap == count - 1
            score = segments[i]["length"] + segments[j]["length"]
            pairs.append((not adjacent, score, segments[i], segments[j]))

    pairs.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return [(item[2], item[3]) for item in pairs]


def build_crack_curves(side_a, side_b, rng, variation, tolerance):
    jitter = clamp(float(variation), 0.0, 1.0) * 0.45
    t_a = clamp(0.5 + rng.uniform(-jitter, jitter), 0.05, 0.95)
    t_b = clamp(0.5 + rng.uniform(-jitter, jitter), 0.05, 0.95)

    pt_a = normalized_point(side_a["curve"], t_a)
    pt_b = normalized_point(side_b["curve"], t_b)

    direction = pt_b - pt_a
    if direction.Length <= tolerance:
        return None, None

    direction.Unitize()

    extension = max(side_a["length"], side_b["length"], pt_a.DistanceTo(pt_b)) * 0.05
    line = rg.Line(pt_a - direction * extension, pt_b + direction * extension)
    display_line = rg.Line(pt_a, pt_b)

    return rg.LineCurve(line), rg.LineCurve(display_line)


def split_once(brep, rng, variation, tolerance):
    segments = outer_boundary_segments(brep)
    pairs = candidate_side_pairs(segments)

    for side_a, side_b in pairs[:10]:
        splitter, display_curve = build_crack_curves(
            side_a,
            side_b,
            rng,
            variation,
            tolerance,
        )
        if splitter is None:
            continue

        splitter_curves = List[rg.Curve]()
        splitter_curves.Add(splitter)
        pieces = brep.Split(splitter_curves, tolerance)
        if not pieces or len(pieces) < 2:
            continue

        valid_pieces = []
        for piece in pieces:
            if brep_area(piece) > tolerance:
                valid_pieces.append(piece)

        if len(valid_pieces) >= 2:
            return valid_pieces, display_curve

    return None, None


def crack_brep(start_brep, smallest_area, depth_limit, variation, random_seed, tolerance):
    rng = random.Random(random_seed)
    pieces = []
    cracks = []
    stack = [(start_brep, 0)]
    attempted = 0

    while stack:
        brep, depth = stack.pop()
        area = brep_area(brep)

        if area <= smallest_area or depth >= depth_limit:
            pieces.append(brep)
            continue

        attempted += 1
        split_pieces, crack = split_once(brep, rng, variation, tolerance)
        if not split_pieces:
            pieces.append(brep)
            continue

        cracks.append(crack)
        for split_piece in split_pieces:
            stack.append((split_piece, depth + 1))

    return pieces, cracks, attempted
