# python being dumb with imports
import random
import time
import json
import ast

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

def stimulation():
    percent = 0

    while percent < 100:
        percent = random.randint(70, 99)  # fluctuate below 100
        stimulation = (
            f"Stimulation : --- INITIATED---, "
            f"Stimulation_status : True;, "
            f"Stimulation : {percent}%"
        )
    prettyPrint(stimulation)
    time.sleep(0.2)