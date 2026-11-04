import cadquery as cq
import os

# Vise Name
vise_name = "My_Vise"

# Parameters for the vise
vise_height = 20
vise_length = 60
vise_width = 15
vise_jaw_height = 10
vise_fixed_jaw_length = 10
vise_sliding_jaw_length = 15
vise_opening = 1

# Parameters for opening range
min_open = 1
max_open = 20
step = 1


def create_vice(
    height=vise_height,
    length=vise_length,
    width=vise_width,
    jaw_height=vise_jaw_height,
    fixed_jaw_length=vise_fixed_jaw_length,
    sliding_jaw_length=vise_sliding_jaw_length,
    opening=vise_opening,
):
    # vise base
    base = (
        cq.Workplane("XY")
        .box(
            width,
            length,
            height - jaw_height,
            centered=(True, False, False)
        )
    )

    # fixed jaw
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

    # sliding jaw
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

vise_folder = f"{vise_name}_step"
os.makedirs(vise_folder, exist_ok=True)

for opening in range(min_open, max_open + 1, step):
    model = create_vice(opening=opening)
    filename = f"{vise_folder}/{vise_name}_{opening}mm.step"
    cq.exporters.export(
        model,
        filename,
        exportType="STEP"
    )
    print(f"\033[92m[OK]\033[0m {filename}")

print("Finished!")
