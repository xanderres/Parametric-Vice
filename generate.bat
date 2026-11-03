@echo off

set OPENSCAD="C:\Program Files\OpenSCAD\openscad.exe"
set SCADFILE=Parametric_Vice.scad

set min_open=1
set max_open=20
set step=1

if not exist stl mkdir stl

for /L %%L in (%min_open%,%step%,%max_open%) do (
    echo Erzeuge STL fuer Opening %%L...
    %OPENSCAD% -D "opening=%%L" -o "stl\vice_%%L.stl" %SCADFILE%
)

echo Fertig!
pause