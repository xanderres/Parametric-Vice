# Parametric Vice

As someone who works with CNC machine programming, I have repeatedly encountered the difficulty of finding suitable vises for machine simulations in CAM systems.

To address this issue, I developed a simple CadQuery-based Python script that generates vise models for a selected range of jaw openings.

The settings can be entered in a Tkinter window:

1. Run the script and enter the vise dimensions and jaw-opening range in the window.
2. Select **Create STEP files for opening range** to export a STEP file for each opening from `min_open` to `max_open`, increasing by `step`, or **Create single STEP file (default opening)** to export only the opening set in `vise_opening`.
3. Import the STEP file for the desired jaw opening into your CAD or CAM software.

This makes it easier to simulate different workpiece setups without having to manually adjust the vise for every configuration.

## Installation

Install Python 3.10 and CadQuery. CadQuery may not yet support the latest Python versions, so an older version may be required.

```bash
pip install cadquery
```

## Script settings

The window displays all settings below. Defaults are still defined near the top of `Parametric_Vice.py`:

| Setting | Default | Description |
|---|---:|---|
| `vise_name` | `"My_Vise"` | Name used for the output folder and files |
| `vise_height` | `20` | Overall vise height |
| `vise_length` | `60` | Base length |
| `vise_width` | `15` | Vise width |
| `vise_jaw_height` | `10` | Jaw height |
| `vise_fixed_jaw_length` | `10` | Fixed jaw length |
| `vise_sliding_jaw_length` | `15` | Sliding jaw length |
| `vise_opening` | `1` | Default opening for `create_vice()`; the export range overrides it |
| `min_open` | `1` | First opening to export |
| `max_open` | `20` | Last opening to export (inclusive) |
| `step` | `1` | Increment in mm between exported openings |

Dimensions are in millimeters. Both buttons save STEP files to a folder named `<vise_name>_step`, using filenames in the format `<vise_name>_<opening>mm.step`.

## Run the Script

Open a terminal in the project folder and run:

```bash
python Parametric_Vice.py
```

The first run can take a very long time while CadQuery starts up and generates the models. Please be patient and allow it to finish. The exported STEP files will be saved in the `<vise_name>_step` folder.