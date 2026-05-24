"""
Recursive ice crack surface splitter for Grasshopper.

Inputs:
    surface: Planar Surface, Brep, BrepFace, or closed planar Curve
    config: Optional multiline config string
    config_text: Optional multiline config string alias
    config_path: Optional path to a text config file
    min_area: Smallest piece area before recursion stops
    max_depth: Maximum recursive split depth
    seed: Random seed for repeatable cracks
    crack_variation: Randomness from 0.0 to 1.0 along selected sides
    tol: Optional model tolerance override

Config format:
    min_area=1.0
    max_depth=8
    seed=1
    crack_variation=0.25
    tol=None

Outputs:
    A: Cracked surface pieces
    B: Crack curves used for successful splits
    C: Final piece areas
    message: Status message
"""
