"""
Automatic script to transfer .strs files into two Excel sheets: "panel" and "stringer".

Note: There may be minor rounding issues (e.g., 0.0448 becoming 0.04 instead of 0.05),
but the script works well for most cases.

Requires: pip install openpyxl
"""

import pandas as pd
import re

def three_decimal_format(value):
    """Format a value as a float with 3 decimals."""
    return f"{float(value):.3f}"

def extract_loadcase_sections(content):
    """Extract each $SUBCASE section from the file content."""
    return re.findall(r"(\$SUBCASE\s+\d+\s+LC\d+.*?)(?=\$SUBCASE|\Z)", content, re.DOTALL)

def parse_stringers(section, subcase_label):
    """Parse stringer element stresses from a section."""
    data = []
    bar_data = re.search(r"\$ELEMENT STRESS\(BAR\) \[REAL\](.*?)\$ELEMENT STRESS", section, re.DOTALL)
    if not bar_data:
        return data

    for line in bar_data.group(1).splitlines():
        parts = re.findall(r"[-+]?\d*\.\d+E[+-]?\d+|[-+]?\d+", line)
        if len(parts) >= 11:
            element_id = int(parts[0])
            if 40 <= element_id <= 66:
                sigma_xx = three_decimal_format(parts[-1])
                stringer_group = (element_id - 40) // 3 + 1
                component_name = f"stringer{stringer_group}"
                data.append([
                    element_id,
                    component_name,
                    sigma_xx,
                    f"Subcase {subcase_label} (LC{subcase_label})"
                ])
    return data

def parse_panels(section, subcase_label):
    """Parse panel element stresses from a section."""
    data = []
    plate_data = re.search(r"\$ELEMENT STRESS\(PLATE\) \[REAL\](.*?)(?=\$SUBCASE|\Z)", section, re.DOTALL)
    if not plate_data:
        return data

    for line in plate_data.group(1).splitlines():
        parts = re.findall(r"[-+]?\d*\.\d+E[+-]?\d+|[-+]?\d+", line)
        if len(parts) == 8:
            element_id = int(parts[0])
            if 1 <= element_id <= 30:
                component_name = f"panel{((element_id - 1) // 3) + 1}"
                """The reason for the rounding error is right here because we only round after we divide the two
                stresses and not beforhand. Not sure if this really is an issue, because the mistakes are minor
                to fix i for now implemented rounding to 3 digits
                """
                xx1, xx2 = float(parts[2]), float(parts[3])
                yy1, yy2 = float(parts[4]), float(parts[5])
                xy1, xy2 = float(parts[6]), float(parts[7])

                xx = three_decimal_format((xx1 + xx2) / 2)
                yy = three_decimal_format((yy1 + yy2) / 2)
                xy = three_decimal_format((xy1 + xy2) / 2)

                data.append([
                    element_id,
                    component_name,
                    xx,
                    yy,
                    xy,
                    f"Subcase {subcase_label} (LC{subcase_label})"
                ])
    return data

def run_get_stresses(name):
    # Read the .strs file
    try:
        with open(f"data/{name}/hmout/input.strs", "r") as file:
            content = file.read()
    except:
        print(f"Error: The file 'data/{name}/hmout/input.strs' does not exist or cannot be read.")

    stringer_all = []
    panel_all = []

    # Process each loadcase section
    for section in extract_loadcase_sections(content):
        match = re.search(r"\$SUBCASE\s+(\d+)", section)
        if match:
            subcase = int(match.group(1))
            stringer_all.extend(parse_stringers(section, subcase))
            panel_all.extend(parse_panels(section, subcase))

    # Create DataFrames
    df_stringer = pd.DataFrame(
        stringer_all,
        columns=["Element ID", "Component Name", "sigmaXX", "Load Case"]
    )
    df_panel = pd.DataFrame(
        panel_all,
        columns=[
            "Element ID", "Component Name", "sigmaXX", "sigmaYY","sigmaXY", "Load Case"
        ]
    )

    # Save to CSV files
    df_stringer.to_csv(f"data/{name}/stringer.csv", index=False)
    df_panel.to_csv(f"data/{name}/panel.csv", index=False)
    #print("CSV files 'stringer.csv' and 'panel.csv' have been created.")

if __name__ == "__main__":
    run_get_stresses()