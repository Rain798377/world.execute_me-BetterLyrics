import random
import json
import sys
import time
import ast

# Function to pretty print JSON objects

def prettyPrint(*args):
    """
    Print any object wrapped in curly braces in a readable format.
    Accepts either a single object (`prettyPrint(obj)`) or a label/object
    pair (`prettyPrint(label, obj)`). Compound objects are pretty-printed
    and each item appears on its own indented line. The opening brace
    is always printed on a new line.
    """
    # Normalize input: support prettyPrint(obj) and prettyPrint(label, obj)
    if len(args) == 0:
        obj = ""
        label = None
    elif len(args) == 1:
        obj = args[0]
        label = None
    else:
        label = args[0]
        obj = args[1]

    try:
        # If object is a compound type, serialize to JSON then extract inner
        if isinstance(obj, (dict, list, tuple, set)):
            if isinstance(obj, (tuple, set)):
                serial = json.dumps(list(obj), indent=4)
            else:
                serial = json.dumps(obj, indent=4)

            lines = serial.splitlines()
            # strip outer braces/brackets
            if len(lines) >= 2 and ((lines[0].strip().startswith('{') and lines[-1].strip().endswith('}')) or (lines[0].strip().startswith('[') and lines[-1].strip().endswith(']'))):
                inner_lines = lines[1:-1]
            else:
                inner_lines = lines

            # indent inner lines 4 spaces, label 4 spaces if present
            if inner_lines:
                indented_inner = "\n".join("    " + line for line in inner_lines)
            else:
                indented_inner = ""

            if label:
                content = f"    {label} :\n" + "\n".join("        " + line for line in inner_lines)
            else:
                content = indented_inner

        else:
            # Strings: try to detect label : value when obj is a string and no explicit label
            if isinstance(obj, str):
                s = obj
                if label is None and " : " in s:
                    label, rhs = s.split(" : ", 1)
                    rhs = rhs.strip()
                    parsed = None
                    try:
                        parsed = ast.literal_eval(rhs)
                    except Exception:
                        parsed = None

                    if parsed is not None and isinstance(parsed, (dict, list, tuple, set)):
                        serial = json.dumps(parsed, indent=4)
                        block_lines = serial.splitlines()
                        content = f"    {label} :\n" + "\n".join("        " + line for line in block_lines)
                    elif "\n" in rhs:
                        lines = rhs.splitlines()
                        content = "    " + label + " :\n" + "\n".join("        " + line for line in lines)
                    elif "," in rhs:
                        parts = [p.strip() for p in rhs.split(",")]
                        content = "    " + label + " :\n" + "\n".join("        " + p for p in parts)
                    else:
                        content = "    " + s
                else:
                    # plain string or label provided
                    if label:
                        content = f"    {label} :\n        {s}"
                    else:
                        if "\n" in s:
                            lines = s.splitlines()
                            content = "\n".join("    " + line for line in lines)
                        elif "," in s:
                            parts = [p.strip() for p in s.split(",")]
                            content = "\n".join("    " + p for p in parts)
                        else:
                            content = "    " + s
            else:
                content = "    " + str(obj)
    except Exception:
        content = "    " + str(obj)

    # Print with opening brace on its own line
    if content:
        print("\n{\n" + content + "\n}")
    else:
        print("\n{\n}")



# Generate plotted points
plotted_points = [
    {"x": round(random.uniform(-2, 4), 1), "y": round(random.uniform(-2, 4), 1)}
    for _ in range(3)
]

# Generate dimension of set points
dimension_set_points = [
    {"x": round(random.uniform(-2, 2), 1), "y": round(random.uniform(2, 4), 1)}
    for _ in range(2)
]

# Generate circle parameters
cx = round(random.uniform(2, 6), 1)  # x-center
cy = round(random.uniform(0, 3), 1)  # y-center
r = round(random.uniform(2, 4), 1)   # radius

plotted_circle = {
    "x_center": cx,
    "y_center": cy,
    "radius": r,
    "equation": f"(x - {cx})**2 + (y + {cy})**2 = {r}**2"
}

# Calculate circumference
circumference = {"circumference": round(2 * 3.14159265359 * r, 10)}

# Generate sine wave
amplitude = round(random.uniform(0.5, 2.0), 1)
frequency = round(random.uniform(0.5, 2.0), 1)
phase_shift = round(random.uniform(0, 3.14), 2)

plotted_sine_wave = {
    "equation": f"y = {amplitude} * sin({frequency} * x + {phase_shift})",
    "amplitude": amplitude,
    "frequency": frequency,
    "phase_shift": phase_shift
}

# Generate tangent expression
tangent_amplitude = round(random.uniform(0.5, 2.0), 2)
tangent_frequency = round(random.uniform(1, 6), 2)
tangent_phase = round(random.uniform(-3, 3), 2)

tangent_expr = {
    "dy/dx": f"{tangent_amplitude} * cos({tangent_frequency}x {tangent_phase:+}) * {tangent_frequency}",
    "amplitude": tangent_amplitude,
    "frequency": tangent_frequency,
    "phase": tangent_phase
}
