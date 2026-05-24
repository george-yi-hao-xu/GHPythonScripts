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

## Bundling multi-file GHPython scripts

Some Grasshopper components are easier to develop as several small Python files,
but still need one single `.py` file for the component.

Use this folder convention:

```text
src/component_name/source/
```

The bundler discovers every folder with that shape. It sorts local modules from
their relative imports, keeps `header.py` first when present, and emits
`component.py` last when possible.

For example, the editable source for `ice_crack` lives in:

```text
src/ice_crack/source/
```

After editing those source files, rebuild that single Grasshopper script:

```powershell
python tools/bundle_ghpython.py ice_crack
```

This regenerates:

```text
src/ice_crack/ice_crack.py
```

To see all discovered components:

```powershell
python tools/bundle_ghpython.py --list
```

To rebuild every discovered component:

```powershell
python tools/bundle_ghpython.py
```

## Component config strings

Some components can read settings from one multiline Grasshopper text input
instead of many separate sliders or panels.

For `ice_crack`, add a text input named `config` or `config_text` with:

```text
min_area=1.0
max_depth=8
seed=1
crack_variation=0.25
tol=None
```

The same text can also live in a `.txt` file, passed through an input named
`config_path`.

If both config text and individual inputs are present, the individual inputs
win when they are filled in.
