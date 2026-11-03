@echo off

set OPENSCAD="C:\Program Files\OpenSCAD\openscad.exe"
set SCADFILE=Parametric_Vice.scad

set min_open=0
set max_open=20
set step=5



if not exist stl mkdir stl

for /L %%L in (%min_open%,%step%,%max_open%) do (
    echo Generate STL for Vice with opening %%L mm
    %OPENSCAD% -D "opening=%%L" -o "stl\vice_%%L.stl" %SCADFILE% >nul 2>&1

    if errorlevel 1 (
        echo   [ERROR]
    ) else (
        echo   [OK]
    )

)

echo Fertig!
pause