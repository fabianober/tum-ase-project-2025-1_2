import numpy as np
import pandas as pd
import os

from formulas.mass import total_mass

# --- Run pipeline ---
from hmscript.change_properties import changeParameters
from hmscript.run_analysis import run_get_properties, run_run_analysis
from calculators.calculate_panels import calculate_panels
from calculators.calculate_stringers import calculate_stringers

def fem_evaluate_vector(
    x,
    person,
    min_rf,
    expected_n_strength=1  # set to nonzero if you want dummy RFs to have specific length
        ):
    """
    x: array-like (length 25): [web_height_1...skin_thickness_5]
    name: str, used as a folder/case name for this run
    
    Returns:
        mass: float
        rf_panel: np.ndarray
        rf_stringer: np.ndarray
        rf_buckling: np.ndarray (if available, else empty)
    """

    # Set output directory
    outdir = f"./data/{person}/output/"

    # --- Convert x to needed argument structure ---
    x = np.array(x).flatten()
    skinThickness = list(x[20:25])
    stringerDim = []
    for i in range(5):
        Dim1 = float(x[i])        # web_height_i
        Dim2 = float(x[15+i])     # thickness_i
        Dim3 = float(x[5+i])      # flange_width_i
        Dim4 = float(x[10+i])     # lip_height_i
        stringerDim.append([Dim1, Dim2, Dim3, Dim4])


    # Change parameters in model
    changeParameters(skinThickness, stringerDim)
    # Compute geometric properties (if needed)
    run_get_properties(person)
    # Run full FEA
    run_run_analysis(person)
    # Calculate panel and stringer results (writes CSV)
    calculate_panels(person)
    calculate_stringers(person)

    #total_mass = total_mass(name=name)
    # Mass (robustly read)
    #mass_file = os.path.join(outdir, "totalMass.txt")
    #if os.path.exists(mass_file):
    #    with open(mass_file, "r") as f:
    #        mass = float(f.read().strip())
    #else:
    #    mass = np.nan #Code didn't find anything nan: "not a number" will throw error for debug
    mass = total_mass(name=person)

    # --- Read PanelRFs.csv ---
    rf_panel = np.array([])
    panel_rfs_file = os.path.join(outdir, "PanelRFs.csv")
    if os.path.exists(panel_rfs_file):
        try:
            df_panel = pd.read_csv(panel_rfs_file)
            if "Reserve Factor" in df_panel.columns:
                rf_panel = df_panel["Reserve Factor"].values
        except Exception as e:
            print(f"Warning: failed to read {panel_rfs_file}: {e}")

    # --- Read StringerRFs.csv ---
    rf_stringer = np.array([])
    stringer_rfs_file = os.path.join(outdir, "StringerRFs.csv")
    if os.path.exists(stringer_rfs_file):
        try:
            df_str = pd.read_csv(stringer_rfs_file)
            if "Reserve Factor" in df_str.columns:
                rf_stringer = df_str["Reserve Factor"].values
        except Exception as e:
            print(f"Warning: failed to read {stringer_rfs_file}: {e}")

    # For stability/buckling: decide mapping according to your convention
    # Let's say panel RFs = stability, stringer RFs = buckling
    rf_stability = np.array(rf_panel, dtype=float)
    rf_buckling = np.array(rf_stringer, dtype=float)

    # --- Strength RFs: always missing, so use dummy vector ---
    if expected_n_strength > 0:
        rf_strength = np.full(expected_n_strength, min_rf, dtype=float)
    else:
        rf_strength = np.array([min_rf], dtype=float)  # or np.array([], dtype=float) if your optimizer accepts

    return mass, rf_strength, rf_stability, rf_buckling