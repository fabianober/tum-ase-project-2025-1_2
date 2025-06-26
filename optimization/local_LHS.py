import pandas as pd
import numpy as np
from pyDOE import lhs
from datetime import datetime
import hm
import os
from Transfer import *

def localLHS(n_samples_in, spread_in, base_input_in, output_csv="lhs_results.csv"):
    csv_columns = [
        'timestamp', 'stage', 'region', 'fem_call_idx',
        'web_height_1', 'web_height_2', 'web_height_3', 'web_height_4', 'web_height_5',
        'flange_width_1', 'flange_width_2', 'flange_width_3', 'flange_width_4', 'flange_width_5',
        'lip_height_1', 'lip_height_2', 'lip_height_3', 'lip_height_4', 'lip_height_5',
        'thickness_1', 'thickness_2', 'thickness_3', 'thickness_4', 'thickness_5',
        'skin_thickness_1', 'skin_thickness_2', 'skin_thickness_3', 'skin_thickness_4', 'skin_thickness_5',
        'weight',
        'rf_strength_0',
        'rf_stability_0', 'rf_stability_1', 'rf_stability_2', 'rf_stability_3', 'rf_stability_4', 'rf_stability_5',
        'rf_stability_6', 'rf_stability_7', 'rf_stability_8', 'rf_stability_9', 'rf_stability_10', 'rf_stability_11',
        'rf_stability_12', 'rf_stability_13', 'rf_stability_14', 'rf_stability_15', 'rf_stability_16', 'rf_stability_17',
        'rf_stability_18', 'rf_stability_19', 'rf_stability_20', 'rf_stability_21', 'rf_stability_22', 'rf_stability_23',
        'rf_stability_24', 'rf_stability_25', 'rf_stability_26', 'rf_stability_27', 'rf_stability_28', 'rf_stability_29',
        'rf_buckling_0', 'rf_buckling_1', 'rf_buckling_2', 'rf_buckling_3', 'rf_buckling_4', 'rf_buckling_5',
        'rf_buckling_6', 'rf_buckling_7', 'rf_buckling_8', 'rf_buckling_9', 'rf_buckling_10', 'rf_buckling_11',
        'rf_buckling_12', 'rf_buckling_13', 'rf_buckling_14', 'rf_buckling_15', 'rf_buckling_16', 'rf_buckling_17',
        'rf_buckling_18', 'rf_buckling_19', 'rf_buckling_20', 'rf_buckling_21', 'rf_buckling_22', 'rf_buckling_23',
        'rf_buckling_24', 'rf_buckling_25', 'rf_buckling_26'
    ]

    # 1. Ensure log directory exists
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(script_dir, "optimizer_logs")
    os.makedirs(log_dir, exist_ok=True)
    output_path = os.path.join(log_dir, output_csv)
    print(f"Saving CSV to: {output_path}")

    # 2. Write the header at the start
    pd.DataFrame(columns=csv_columns).to_csv(output_path, index=False)

    # 3. Generate LHS samples
    base_input = base_input_in
    spread = spread_in
    n_samples = n_samples_in

    input_lows = [x * (1 - spread) for x in base_input]
    input_highs = [x * (1 + spread) for x in base_input]
    lhs_samples = lhs(len(base_input), samples=n_samples)
    X = lhs_samples * (np.array(input_highs) - np.array(input_lows)) + np.array(input_lows)

    # 4. Write each row as soon as it's ready (append mode, header=False)
    for i, x in enumerate(X):
        result = fem_evaluate_vector(list(x), "felix", 1.05)
        row = {}
        row["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row["stage"] = "Frontier_sampling"
        row["region"] = -1
        row["fem_call_idx"] = i

        row["web_height_1"] = x[0]
        row["web_height_2"] = x[1]
        row["web_height_3"] = x[2]
        row["web_height_4"] = x[3]
        row["web_height_5"] = x[4]
        row["flange_width_1"] = x[5]
        row["flange_width_2"] = x[6]
        row["flange_width_3"] = x[7]
        row["flange_width_4"] = x[8]
        row["flange_width_5"] = x[9]
        row["lip_height_1"] = x[10]
        row["lip_height_2"] = x[11]
        row["lip_height_3"] = x[12]
        row["lip_height_4"] = x[13]
        row["lip_height_5"] = x[14]
        row["thickness_1"] = x[15]
        row["thickness_2"] = x[16]
        row["thickness_3"] = x[17]
        row["thickness_4"] = x[18]
        row["thickness_5"] = x[19]
        row["skin_thickness_1"] = x[20]
        row["skin_thickness_2"] = x[21]
        row["skin_thickness_3"] = x[22]
        row["skin_thickness_4"] = x[23]
        row["skin_thickness_5"] = x[24]

        row["weight"] = result[0]
        row["rf_strength_0"] = result[1][0]
        stability = result[2]
        for j in range(30):
            row[f"rf_stability_{j}"] = stability[j]
        buckling = result[3]
        for j in range(27):
            row[f"rf_buckling_{j}"] = buckling[j]

        # Write just this row (append mode)
        pd.DataFrame([row], columns=csv_columns).to_csv(output_path, mode='a', header=False, index=False)

# Example usage:
# localLHS(
#     250,
#     0.10,
#     [28,28,28,29,29,25,25,26,26,26,6,6,6,6,6,5,5,5,5,5,5,4.8,5,5,5.5],
#     output_csv="lhs_results.csv"
# )

def localLHS_variable_spread(n_samples_in, spreads_in, base_input_in, output_csv="lhs_results.csv"):
    """
    Same as localLHS, but allows for individual spread for each variable.
    spreads_in: List/array of 25 spreads, one per variable.
    """
    csv_columns = [
        'timestamp', 'stage', 'region', 'fem_call_idx',
        'web_height_1', 'web_height_2', 'web_height_3', 'web_height_4', 'web_height_5',
        'flange_width_1', 'flange_width_2', 'flange_width_3', 'flange_width_4', 'flange_width_5',
        'lip_height_1', 'lip_height_2', 'lip_height_3', 'lip_height_4', 'lip_height_5',
        'thickness_1', 'thickness_2', 'thickness_3', 'thickness_4', 'thickness_5',
        'skin_thickness_1', 'skin_thickness_2', 'skin_thickness_3', 'skin_thickness_4', 'skin_thickness_5',
        'weight',
        'rf_strength_0',
        'rf_stability_0', 'rf_stability_1', 'rf_stability_2', 'rf_stability_3', 'rf_stability_4', 'rf_stability_5',
        'rf_stability_6', 'rf_stability_7', 'rf_stability_8', 'rf_stability_9', 'rf_stability_10', 'rf_stability_11',
        'rf_stability_12', 'rf_stability_13', 'rf_stability_14', 'rf_stability_15', 'rf_stability_16', 'rf_stability_17',
        'rf_stability_18', 'rf_stability_19', 'rf_stability_20', 'rf_stability_21', 'rf_stability_22', 'rf_stability_23',
        'rf_stability_24', 'rf_stability_25', 'rf_stability_26', 'rf_stability_27', 'rf_stability_28', 'rf_stability_29',
        'rf_buckling_0', 'rf_buckling_1', 'rf_buckling_2', 'rf_buckling_3', 'rf_buckling_4', 'rf_buckling_5',
        'rf_buckling_6', 'rf_buckling_7', 'rf_buckling_8', 'rf_buckling_9', 'rf_buckling_10', 'rf_buckling_11',
        'rf_buckling_12', 'rf_buckling_13', 'rf_buckling_14', 'rf_buckling_15', 'rf_buckling_16', 'rf_buckling_17',
        'rf_buckling_18', 'rf_buckling_19', 'rf_buckling_20', 'rf_buckling_21', 'rf_buckling_22', 'rf_buckling_23',
        'rf_buckling_24', 'rf_buckling_25', 'rf_buckling_26'
    ]

    # 1. Ensure log directory exists
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(script_dir, "optimizer_logs")
    os.makedirs(log_dir, exist_ok=True)
    output_path = os.path.join(log_dir, output_csv)
    print(f"Saving CSV to: {output_path}")

    # 2. Write the header at the start
    pd.DataFrame(columns=csv_columns).to_csv(output_path, index=False)

    # 3. Generate LHS samples
    base_input = base_input_in
    spreads = spreads_in
    n_samples = n_samples_in

    # Compute variable-specific lows and highs
    input_lows = [x * (1 - s) for x, s in zip(base_input, spreads)]
    input_highs = [x * (1 + s) for x, s in zip(base_input, spreads)]
    lhs_samples = lhs(len(base_input), samples=n_samples)
    X = lhs_samples * (np.array(input_highs) - np.array(input_lows)) + np.array(input_lows)

    # 4. Write each row as soon as it's ready (append mode, header=False)
    for i, x in enumerate(X):
        result = fem_evaluate_vector(list(x), "felix", 1.05)
        row = {}
        row["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row["stage"] = "Frontier_sampling"
        row["region"] = -1
        row["fem_call_idx"] = i

        row["web_height_1"] = x[0]
        row["web_height_2"] = x[1]
        row["web_height_3"] = x[2]
        row["web_height_4"] = x[3]
        row["web_height_5"] = x[4]
        row["flange_width_1"] = x[5]
        row["flange_width_2"] = x[6]
        row["flange_width_3"] = x[7]
        row["flange_width_4"] = x[8]
        row["flange_width_5"] = x[9]
        row["lip_height_1"] = x[10]
        row["lip_height_2"] = x[11]
        row["lip_height_3"] = x[12]
        row["lip_height_4"] = x[13]
        row["lip_height_5"] = x[14]
        row["thickness_1"] = x[15]
        row["thickness_2"] = x[16]
        row["thickness_3"] = x[17]
        row["thickness_4"] = x[18]
        row["thickness_5"] = x[19]
        row["skin_thickness_1"] = x[20]
        row["skin_thickness_2"] = x[21]
        row["skin_thickness_3"] = x[22]
        row["skin_thickness_4"] = x[23]
        row["skin_thickness_5"] = x[24]

        row["weight"] = result[0]
        row["rf_strength_0"] = result[1][0]
        stability = result[2]
        for j in range(30):
            row[f"rf_stability_{j}"] = stability[j]
        buckling = result[3]
        for j in range(27):
            row[f"rf_buckling_{j}"] = buckling[j]

        # Write just this row (append mode)
        pd.DataFrame([row], columns=csv_columns).to_csv(output_path, mode='a', header=False, index=False)

# Example usage:
# localLHS_variable_spread(
#     250,
#     [0.10,0.10,0.10,0.10,0.10, 0.05,0.05,0.05,0.05,0.05, 0.08,0.08,0.08,0.08,0.08, 0.03,0.03,0.03,0.03,0.03, 0.10,0.10,0.10,0.10,0.10],
#     [28,28,28,29,29,25,25,26,26,26,6,6,6,6,6,5,5,5,5,5,5,4.8,5,5,5.5],
#     output_csv="lhs_results_variable_spread.csv"
# )

import pandas as pd
import numpy as np
from pyDOE import lhs
from datetime import datetime
import os
import gc
import psutil
from Transfer import *

def localLHS_variable_spread_LR(n_samples_in, spreads_in, base_input_in, output_csv="lhs_results.csv"):
    """
    Latin Hypercube Sampling with variable spread per variable.
    Each variable gets its own spread from spreads_in (same length as base_input_in).
    Writes each result immediately to CSV to avoid memory bloat.
    Prints RAM usage per iteration for debugging.

    Args:
        n_samples_in: Number of samples to generate
        spreads_in: List/array of relative spreads (fraction, e.g. 0.1 means +/-10%) per variable
        base_input_in: List/array of base variable values (length N)
        output_csv: Output CSV filename
    """
    csv_columns = [
        'timestamp', 'stage', 'region', 'fem_call_idx',
        'web_height_1', 'web_height_2', 'web_height_3', 'web_height_4', 'web_height_5',
        'flange_width_1', 'flange_width_2', 'flange_width_3', 'flange_width_4', 'flange_width_5',
        'lip_height_1', 'lip_height_2', 'lip_height_3', 'lip_height_4', 'lip_height_5',
        'thickness_1', 'thickness_2', 'thickness_3', 'thickness_4', 'thickness_5',
        'skin_thickness_1', 'skin_thickness_2', 'skin_thickness_3', 'skin_thickness_4', 'skin_thickness_5',
        'weight',
        'rf_strength_0',
        *[f'rf_stability_{j}' for j in range(30)],
        *[f'rf_buckling_{j}' for j in range(27)],
    ]

    # 1. Ensure log directory exists
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(script_dir, "optimizer_logs")
    os.makedirs(log_dir, exist_ok=True)
    output_path = os.path.join(log_dir, output_csv)
    print(f"Saving CSV to: {output_path}")

    # 2. Write the header at the start
    pd.DataFrame(columns=csv_columns).to_csv(output_path, index=False)

    # 3. Generate LHS samples (variable spread)
    base_input = np.array(base_input_in)
    spreads = np.array(spreads_in)
    n_samples = n_samples_in

    # Individual low/high per variable
    input_lows = base_input * (1 - spreads)
    input_highs = base_input * (1 + spreads)
    lhs_samples = lhs(len(base_input), samples=n_samples)
    X = lhs_samples * (input_highs - input_lows) + input_lows

    process = psutil.Process(os.getpid())

    # 4. Write each row as soon as it's ready (append mode, header=False)
    for i, x in enumerate(X):
        result = fem_evaluate_vector(list(x), "felix", 1.05)
        row = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "stage": "Frontier_sampling",
            "region": -1,
            "fem_call_idx": i,
        }

        for idx, key in enumerate([
            'web_height_1', 'web_height_2', 'web_height_3', 'web_height_4', 'web_height_5',
            'flange_width_1', 'flange_width_2', 'flange_width_3', 'flange_width_4', 'flange_width_5',
            'lip_height_1', 'lip_height_2', 'lip_height_3', 'lip_height_4', 'lip_height_5',
            'thickness_1', 'thickness_2', 'thickness_3', 'thickness_4', 'thickness_5',
            'skin_thickness_1', 'skin_thickness_2', 'skin_thickness_3', 'skin_thickness_4', 'skin_thickness_5'
        ]):
            row[key] = x[idx]

        row["weight"] = result[0]
        row["rf_strength_0"] = result[1][0]
        stability = result[2]
        for j in range(30):
            row[f"rf_stability_{j}"] = stability[j]
        buckling = result[3]
        for j in range(27):
            row[f"rf_buckling_{j}"] = buckling[j]

        # Write just this row (append mode)
        temp_df = pd.DataFrame([row], columns=csv_columns)
        temp_df.to_csv(output_path, mode='a', header=False, index=False)
        del temp_df  # Explicitly delete DataFrame

        # Show memory usage every iteration (prints in HyperMesh console)
        #print(f"Iteration {i}: RSS = {process.memory_info().rss / 1024 ** 2:.2f} MB")

        # Run garbage collection to free memory
        gc.collect()
