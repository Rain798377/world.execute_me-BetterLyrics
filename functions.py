import random
import json
import sys
import time
import ast

# Function to pretty print JSON objects

import random
import json
import sys
import time
import ast

# Function to pretty print JSON objects

def prettyPrint(*args):
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

            # Keep the outer braces/brackets from the serialized form
            lines = serial.splitlines()

            # Indent every serialized line by 4 spaces when no label is given.
            indented_lines = "\n".join("    " + line for line in lines) if lines else ""

            # If this is a list of dicts, format as bracket with inner brace blocks
            if isinstance(obj, list) and all(isinstance(item, dict) for item in obj):
                def format_dict_block(d, indent_level=12):
                    inner = []
                    for k, v in d.items():
                        inner.append((' ' * (indent_level + 4)) + f"{k}={v}")
                    return (' ' * indent_level) + "{" + "\n" + "\n".join(inner) + "\n" + (' ' * indent_level) + "}"

                inner_blocks = "\n".join(format_dict_block(d, indent_level=12) for d in obj)
                if label:
                    content = f"    {label} :\n" + "        [\n" + inner_blocks + "\n        ]"
                else:
                    content = "    [\n" + inner_blocks + "\n    ]"
            else:
                # If a label is provided, print the label then the serialized block
                if label:
                    content = f"    {label} :\n" + "\n".join("        " + line for line in lines)
                else:
                    content = indented_lines

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

                        # Try to detect repeated key=value patterns and group them into dict blocks
                        def try_group_keyvals(parts):
                            keys = []
                            kvs = []
                            for part in parts:
                                if "=" not in part:
                                    return None
                                k, v = part.split("=", 1)
                                keys.append(k.strip())
                                kvs.append((k.strip(), v.strip()))

                            # find repeating key cycle by scanning until first key repeats
                            cycle_keys = []
                            for k, _ in kvs:
                                if k in cycle_keys:
                                    break
                                cycle_keys.append(k)

                            if not cycle_keys:
                                return None

                            if len(kvs) % len(cycle_keys) != 0:
                                return None

                            groups = []
                            for i in range(0, len(kvs), len(cycle_keys)):
                                group = {}
                                for j, key in enumerate(cycle_keys):
                                    _, val = kvs[i + j]
                                    # try numeric conversion
                                    try:
                                        if "." in val:
                                            v = float(val)
                                        else:
                                            v = int(val)
                                    except Exception:
                                        v = val
                                    group[key] = v
                                groups.append(group)
                            return groups

                        grouped = try_group_keyvals(parts)
                        if grouped is not None:
                            inner_blocks = []
                            for d in grouped:
                                inner = []
                                for k, v in d.items():
                                    inner.append("                " + f"{k}={v}")
                                inner_blocks.append("            {\n" + "\n".join(inner) + "\n            }")

                            content = (
                                "    " + label + " :\n"
                                + "        [\n"
                                + "\n".join(inner_blocks)
                                + "\n        ]"
                            )
                        else:
                            content = (
                                "    " + label + " :\n"
                                + "        [\n"
                                + "\n".join("            " + p for p in parts)
                                + "\n        ]"
                            )
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

                            # Same grouping logic for unlabeled comma strings
                            def try_group_keyvals_unlabeled(parts):
                                keys = []
                                kvs = []
                                for part in parts:
                                    if "=" not in part:
                                        return None
                                    k, v = part.split("=", 1)
                                    keys.append(k.strip())
                                    kvs.append((k.strip(), v.strip()))

                                cycle_keys = []
                                for k, _ in kvs:
                                    if k in cycle_keys:
                                        break
                                    cycle_keys.append(k)
                                if not cycle_keys or len(kvs) % len(cycle_keys) != 0:
                                    return None
                                groups = []
                                for i in range(0, len(kvs), len(cycle_keys)):
                                    group = {}
                                    for j, key in enumerate(cycle_keys):
                                        _, val = kvs[i + j]
                                        try:
                                            if "." in val:
                                                v = float(val)
                                            else:
                                                v = int(val)
                                        except Exception:
                                            v = val
                                        group[key] = v
                                    groups.append(group)
                                return groups

                            grouped = try_group_keyvals_unlabeled(parts)
                            if grouped is not None:
                                inner_blocks = []
                                for d in grouped:
                                    inner = []
                                    for k, v in d.items():
                                        inner.append("        " + f"{k}={v}")
                                    inner_blocks.append("    {\n" + "\n".join(inner) + "\n    }")
                                content = "    [\n" + "\n".join(inner_blocks) + "\n    ]"
                            else:
                                content = "    [\n" + "\n".join("        " + p for p in parts) + "\n    ]"
                        else:
                            content = "    " + s
            else:
                content = "    " + str(obj)
    except Exception:
        content = "    " + str(obj)

    if content:
        print("\n{\n" + content + "\n}")
    else:
        print("\n{\n}")


# Generate plotted points
plotted_points = ", ".join(f"x={round(random.uniform(-2, 4),1)}, y={round(random.uniform(-2, 4),1)}" for _ in range(3))

# Generate 2 random dimension set points
dimension_set_points = ", ".join(f"x={round(random.uniform(-2, 2),1)}, y={round(random.uniform(2, 4),1)}" for _ in range(2))

# Circle parameters
cx = round(random.uniform(2, 6),1)
cy = round(random.uniform(0, 3),1)
r = round(random.uniform(2, 4),1)
plotted_circle = f"x_center = {cx}, y_center = {cy}, radius = {r}, equation = (x - {cx})**2 + (y - {cy})**2 = {r}**2"
circumference = round(2 * 3.14159265359 * r, 10)

# Sine wave
amplitude = round(random.uniform(0.5, 2.0),1)
frequency = round(random.uniform(0.5, 2.0),1)
phase_shift = round(random.uniform(0, 3.14),2)
plotted_sine_wave = f"y = {amplitude} * sin({frequency} * x + {phase_shift}), amplitude = {amplitude}, frequency = {frequency}, phase_shift = {phase_shift}"

# Tangent expression
tangent_amplitude = round(random.uniform(0.5, 2.0),2)
tangent_frequency = round(random.uniform(1, 6),2)
tangent_phase = round(random.uniform(-3, 3),2)
tangent_expr = f"dy/dx = {tangent_amplitude} * cos({tangent_frequency}x {tangent_phase:+}) * {tangent_frequency}, amplitude = {tangent_amplitude}, frequency = {tangent_frequency}, phase = {tangent_phase}"

# random limit.
rand_limit = random.randint(100, 500)

import random

# Speed of light in meters per second
c = 299_792_458  

def random_years():
    # Random BC year between 1000 BC and 1 BC
    bc_year = random.randint(1, 1000)
    # Random AD year between 1 AD and 3000 AD
    ad_year = random.randint(1, 3000)
    return bc_year, ad_year

def time_to_travel(bc_year, ad_year, speed):
    # Convert years to seconds assuming 1 year = 365.25 days
    years_diff = ad_year + bc_year  # BC to AD crossing
    seconds = years_diff * 365.25 * 24 * 60 * 60
    # Distance = speed * time, so time = distance / speed
    # Let's assume distance = years_diff in light-years converted to meters
    # 1 light-year = speed_of_light * 1 year
    distance_m = years_diff * c * 365.25 * 24 * 60 * 60
    time_seconds = distance_m / speed
    return time_seconds
# Random years
bc, ad = random_years()
# Compute time at speed of light
time_sec = time_to_travel(bc, ad, c)
