import random
import json
import sys
import time
import ast
import math



import json
import ast

def prettyPrint(*args):
    """
    Pretty-print an object with braces and indentation.
    - Accepts prettyPrint(obj) or prettyPrint(label, obj)
    - Compound objects and comma-separated strings are printed one item per line
    - Opening brace is always on its own line
    """
    # Handle input
    if len(args) == 0:
        label = None
        obj = ""
    elif len(args) == 1:
        label = None
        obj = args[0]
    else:
        label, obj = args

    def format_obj(o, indent=4):
        """Recursively format compound objects or comma-separated strings."""
        space = " " * indent
        # Handle dict, list, tuple, set
        if isinstance(o, (dict, list, tuple, set)):
            # Convert tuple/set to list for JSON
            serial = json.dumps(list(o) if isinstance(o, (tuple, set)) else o, indent=4)
            lines = serial.splitlines()
            # Remove outer braces/brackets
            if len(lines) >= 2 and ((lines[0].strip().startswith('{') and lines[-1].strip().endswith('}')) 
                                    or (lines[0].strip().startswith('[') and lines[-1].strip().endswith(']'))):
                lines = lines[1:-1]
            return "\n".join(space + line for line in lines)
        # Handle comma-separated strings
        elif isinstance(o, str) and "," in o:
            parts = [p.strip() for p in o.split(",")]
            return "\n".join(space + p for p in parts)
        else:
            return space + str(o)

    # Handle strings that might contain structured data like "label : {...}"
    if isinstance(obj, str) and label is None and " : " in obj:
        try:
            l, rhs = obj.split(" : ", 1)
            rhs_parsed = ast.literal_eval(rhs)
            if isinstance(rhs_parsed, (dict, list, tuple, set)):
                label = l
                obj = rhs_parsed
        except Exception:
            pass

    # Build content
    if label:
        content = f"    {label} :\n" + format_obj(obj, indent=8)
    else:
        content = format_obj(obj, indent=4)

    # Print with opening brace on its own line
    print("\n{\n" + content + "\n}")



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
plotted_sine_wave = f",y = {amplitude} * sin({frequency} * x + {phase_shift}), amplitude = {amplitude}, frequency = {frequency}, phase_shift = {phase_shift}"

# Tangent expression
tangent_amplitude = round(random.uniform(0.5, 2.0),2)
tangent_frequency = round(random.uniform(1, 6),2)
tangent_phase = round(random.uniform(-3, 3),2)
tangent_expr = f",dy/dx = {tangent_amplitude} * cos({tangent_frequency}x {tangent_phase:+}) * {tangent_frequency}, amplitude = {tangent_amplitude}, frequency = {tangent_frequency}, phase = {tangent_phase}"

# Tangent (derivative-like) callable
tangent = lambda x: tangent_amplitude * tangent_frequency * math.cos(
    tangent_frequency * x + tangent_phase
)


# Compute derived values for the generated shapes/functions
circle_area = math.pi * r * r
# Choose a point on the circle at angle 0 (to the right of center) and verify equation
point_on_circle = (round(cx + r, 6), round(cy, 6))
circle_eq_value = (point_on_circle[0] - cx) ** 2 + (point_on_circle[1] - cy) ** 2

# Define sine function and sample both sine and tangent at a few x values
sine = lambda x: amplitude * math.sin(frequency * x + phase_shift)
sample_xs = [0, 1, 2]
sine_samples = {x: round(sine(x), 6) for x in sample_xs}
tangent_samples = {x: round(tangent(x), 6) for x in sample_xs}

computed = {
    "circle_area": round(circle_area, 6),
    "circumference": circumference,
    "point_on_circle": point_on_circle,
    "circle_eq_value": round(circle_eq_value, 6),
    "plotted_circle": plotted_circle,
    "plotted_sine_wave": plotted_sine_wave,
    "tangent_expr": tangent_expr,
    "sine_samples": sine_samples,
    "tangent_samples": tangent_samples,
}



# random limit.
rand_limit = random.randint(100, 500)


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

stimulation = "Stimulation:, --- INITIATED---, Stimulation_status : True;, Stimulation : 100%"
satisfaction = "Satisfaction:, --- INITIATED---, Satisfaction_status : True;, Satisfaction : 100%"
happiness = "Happiness:, --- INITIATED---, Happiness_status : True;, Happiness : 100%"
execution = "Execution:, --- INITIATED ---, Emotions : ENABLED;"