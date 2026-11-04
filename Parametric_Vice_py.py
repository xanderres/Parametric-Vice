import cadquery as cq
import os


def create_vice(
    height=20,
    length=60,
    width=15,
    jaw_height=10,
    fixed_jaw_length=10,
    sliding_jaw_length=15,
    opening=1,
):
    # Grundkörper
    base = (
        cq.Workplane("XY")
        .box(
            width,
            length,
            height - jaw_height,
            centered=(True, False, False)
        )
    )

    # Feste Backe
    fixed_jaw = (
        cq.Workplane("XY")
        .box(
            width,
            fixed_jaw_length,
            height,
            centered=(True, False, False)
        )
    )

    base_fixed_jaw = base.union(fixed_jaw)

    # Bewegliche Backe
    sliding_jaw = (
        cq.Workplane("XY")
        .transformed(
            offset=(
                0,
                fixed_jaw_length + opening + sliding_jaw_length / 2,
                height - jaw_height + (height - jaw_height) / 2,
            )
        )
        .box(
            width,
            sliding_jaw_length,
            height - jaw_height,
            centered=True
        )
    )

    return base_fixed_jaw.union(sliding_jaw)


# Parameterbereich
min_open = 0
max_open = 20
step = 5

os.makedirs("step", exist_ok=True)

for opening in range(min_open, max_open + 1, step):

    model = create_vice(opening=opening)

    filename = f"step/vice_{opening}.step"

    cq.exporters.export(
        model,
        filename,
        exportType="STEP"
    )

    print(f"[OK] {filename}")

print("Fertig!")

input("Press Enter to continue...")