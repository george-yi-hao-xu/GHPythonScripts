# GHPythonScripts

A collection of Python scripts for Rhino Grasshopper.

## Setup

Create and activate a virtual environment if you do not already have one:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install development-only editor helpers:

```powershell
python -m pip install -r requirements-dev.txt
```

After the virtual environment is activated, you can use `python` directly. If the environment is not activated, use the explicit interpreter path:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

`requirements-dev.txt` contains Rhino/Grasshopper stub packages used for VS Code autocomplete and type hints, such as:

```python
import Rhino.Geometry as rg
```

These stubs do not provide the real Rhino runtime. Rhino and Grasshopper provide `Rhino.Geometry` when the scripts run inside Rhino.

## Grasshopper inputs and type hints

Grasshopper component inputs are injected into the script as global variables at runtime. Pylance cannot see those injected names when it analyzes the file in VS Code, so a plain input such as `points` or `curve` may be reported as undefined or unbound.

Use `globals()` with type comments to bind the injected value while giving Pylance a useful type:

```python
import Rhino.Geometry as rg

points = globals()["points"]  # type: list[rg.Point3d]
curve = globals()["curve"]  # type: rg.Curve
```

`globals()["points"]` retrieves the value that Grasshopper injected into the script namespace. The `# type: ...` comments are read by Pylance, but ignored by Grasshopper at runtime.

If the script is run outside Grasshopper, this pattern will raise a `KeyError` unless those globals are provided another way.

Keep `requirements.txt` for actual pip packages needed at runtime.
