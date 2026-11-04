# Parametric Vice

A parametric vise generator for CAM simulations. The Python script creates 3D vise models for multiple jaw opening widths and exports them as STEP files.

## Requirements

- Windows (the commands below use PowerShell)
- Python 3.10 or newer
- CadQuery

## Installation

1. Install Python from [python.org](https://www.python.org/downloads/). During installation, enable the **Add Python to PATH** option.
2. Open PowerShell in the project directory.
3. Create and activate a virtual environment:

   ```powershell
   py -3.10 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks script activation, you can invoke Python directly using `.\.venv\Scripts\python.exe`.
4. Install CadQuery:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install cadquery
   ```

## Usage

Run the script from the project directory:

```powershell
python .\Parametric_Vice_py.py
```

The script creates the `step` directory if needed and saves a STEP file there for each jaw opening width, for example `step/vice_0.step`. The filename is printed in the terminal after each successful export. At the end, the script waits for you to press Enter.

The files can be imported into any CAD or CAM application that supports STEP.

## Customizing Parameters

Open `Parametric_Vice_py.py` and edit the parameter range near the end of the file:

```python
min_open = 0
max_open = 20
step = 5
```

With these values, the script exports models with jaw openings from 0 to 20 inclusive, in increments of 5. `step` must be greater than 0.

The vise dimensions are set by the default values in `create_vice`:

| Parameter | Default | Description |
|---|---:|---|
| `height` | 20 | Overall height |
| `length` | 60 | Length of the base |
| `width` | 15 | Width of the vise |
| `jaw_height` | 10 | Height of the fixed jaw extending above the base |
| `fixed_jaw_length` | 10 | Length of the fixed jaw |
| `sliding_jaw_length` | 15 | Length of the movable jaw |
| `opening` | 1 | Gap between the jaws; during export, this is set by the jaw opening range |

Dimensions use CadQuery model units (millimeters by default). To use different dimensions, edit the values directly in the `create_vice` function definition.
