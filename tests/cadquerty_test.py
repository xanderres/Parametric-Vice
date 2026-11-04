import cadquery as cq

cube = cq.Workplane("XY").box(10, 10, 10)

cq.exporters.export(cube, "cube.step")

print("cube.step wurde erstellt.")