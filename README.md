Parametric Vice

A parametric vise generator primarily designed for CAM applications.

Overview

As someone who works with CNC machine programming, I have repeatedly encountered the difficulty of finding suitable vises for machine simulations in CAM systems.

To address this issue, I developed a relatively simple OpenSCAD script that allows you to generate a parametric vise in a predefined range of jaw opening positions.

The idea is simple:

1. Configure the vise according to your requirements.
2. Run the generation script, which automatically creates the vise at different jaw opening positions using a user-defined step size.
3. Import the generated vise models into your CAM system and select the appropriate jaw opening for your simulation.

This makes it easier to simulate different workpiece setups without having to manually adjust the vise for every configuration.

Installation & Usage

1. Install OpenSCAD on your system.
2. Download the complete Git repository.
    Open the OpenSCAD (.scad) file and enter your desired vise dimensions and parameters.
3. Run the generation script.
    The script will automatically generate STL files for all defined jaw opening positions.
4. Import the STL files into your CAM system.
    Select the appropriate vise opening and position your workpiece accordingly.

Features

* Parametric vise geometry
* Customizable vise dimensions
* Configurable jaw opening range
* User-defined step size
* Automatic STL generation
* Designed for use in CAM simulations