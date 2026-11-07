import queue
import re
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

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
    import cadquery as cq

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


def validate_settings(settings):
    name = settings["vise_name"]
    if (
        not name.strip()
        or name != name.strip()
        or re.search(r'[<>:"/\\|?*]', name)
        or name.endswith(".")
    ):
        raise ValueError("The vise name cannot be empty or contain invalid filename characters.")

    positive_values = (
        "vise_height",
        "vise_length",
        "vise_width",
        "vise_jaw_height",
        "vise_fixed_jaw_length",
        "vise_sliding_jaw_length",
        "vise_opening",
        "min_open",
        "max_open",
        "step",
    )
    for key in positive_values:
        if settings[key] <= 0:
            raise ValueError(f"{key} must be greater than 0.")

    if settings["vise_jaw_height"] >= settings["vise_height"]:
        raise ValueError("Jaw height must be less than the overall vise height.")
    if settings["min_open"] > settings["max_open"]:
        raise ValueError("Minimum opening cannot be greater than maximum opening.")


def generate_models(settings, progress_callback=None):
    import cadquery as cq

    validate_settings(settings)
    output_folder = Path(f'{settings["vise_name"]}_step')
    output_folder.mkdir(parents=True, exist_ok=True)

    openings = range(
        settings["min_open"],
        settings["max_open"] + 1,
        settings["step"],
    )
    for opening in openings:
        model = create_vice(
            height=settings["vise_height"],
            length=settings["vise_length"],
            width=settings["vise_width"],
            jaw_height=settings["vise_jaw_height"],
            fixed_jaw_length=settings["vise_fixed_jaw_length"],
            sliding_jaw_length=settings["vise_sliding_jaw_length"],
            opening=opening,
        )
        filename = output_folder / f'{settings["vise_name"]}_{opening}mm.step'
        cq.exporters.export(model, str(filename), exportType="STEP")
        if progress_callback:
            progress_callback(f"Exported: {filename}")

    return output_folder


PARAMETER_FIELDS = (
    ("Vise name", "vise_name", str),
    ("Vise height (mm)", "vise_height", int),
    ("Vise length (mm)", "vise_length", int),
    ("Vise width (mm)", "vise_width", int),
    ("Jaw height (mm)", "vise_jaw_height", int),
    ("Fixed jaw length (mm)", "vise_fixed_jaw_length", int),
    ("Sliding jaw length (mm)", "vise_sliding_jaw_length", int),
    ("Default opening (mm)", "vise_opening", int),
    ("Minimum opening (mm)", "min_open", int),
    ("Maximum opening (mm)", "max_open", int),
    ("Step size (mm)", "step", int),
)


def launch_gui():
    root = tk.Tk()
    root.title("Parametric Vice")
    root.resizable(False, False)
    root.columnconfigure(1, weight=1)

    variables = {}
    for row, (label, key, _value_type) in enumerate(PARAMETER_FIELDS):
        ttk.Label(root, text=label).grid(
            row=row,
            column=0,
            padx=(12, 8),
            pady=5,
            sticky="w",
        )
        variable = tk.StringVar(value=str(globals()[key]))
        variables[key] = variable
        ttk.Entry(root, textvariable=variable, width=24).grid(
            row=row,
            column=1,
            padx=(0, 12),
            pady=5,
            sticky="ew",
        )

    status = tk.StringVar(
        value="The selected opening range will be exported. The default opening is used by create_vice()."
    )
    ttk.Label(root, textvariable=status, wraplength=400).grid(
        row=len(PARAMETER_FIELDS),
        column=0,
        columnspan=2,
        padx=12,
        pady=(8, 4),
        sticky="w",
    )

    messages = queue.Queue()

    def collect_settings():
        settings = {}
        for _label, key, value_type in PARAMETER_FIELDS:
            raw_value = variables[key].get()
            try:
                settings[key] = value_type(raw_value) if value_type is int else raw_value
            except ValueError as error:
                raise ValueError(f"Invalid value for {key}: {raw_value}") from error
        validate_settings(settings)
        return settings

    def poll_messages():
        try:
            while True:
                kind, value = messages.get_nowait()
                if kind == "progress":
                    status.set(value)
                elif kind == "done":
                    status.set(f"Done. STEP files saved to: {value}")
                    generate_button.configure(state="normal")
                elif kind == "error":
                    status.set("Export failed.")
                    generate_button.configure(state="normal")
                    messagebox.showerror("Export failed", str(value), parent=root)
        except queue.Empty:
            pass
        if generate_button.instate(["disabled"]):
            root.after(100, poll_messages)

    def start_generation():
        try:
            settings = collect_settings()
        except ValueError as error:
            messagebox.showerror("Invalid settings", str(error), parent=root)
            return

        generate_button.configure(state="disabled")
        status.set("Preparing export...")

        def worker():
            try:
                output_folder = generate_models(
                    settings,
                    lambda message: messages.put(("progress", message)),
                )
                messages.put(("done", output_folder))
            except Exception as error:
                messages.put(("error", error))

        threading.Thread(target=worker, daemon=True).start()
        root.after(100, poll_messages)

    generate_button = ttk.Button(root, text="Create STEP files", command=start_generation)
    generate_button.grid(
        row=len(PARAMETER_FIELDS) + 1,
        column=0,
        columnspan=2,
        padx=12,
        pady=(4, 12),
        sticky="ew",
    )

    root.mainloop()


if __name__ == "__main__":
    launch_gui()
