import joblib
import numpy as np
import os

# Automatically load the models the first time this module is imported
_here = os.path.dirname(__file__)
rf_weight = joblib.load(os.path.join(_here, "rf_weight_model.joblib"))
rf_rf = joblib.load(os.path.join(_here, "rf_rf_model.joblib"))

def predict_rf_and_weight(input_vector):
    """
    input_vector: list or array of 25 floats (inputs in the same order as during training)
    returns: (predicted_min_nonstrength_rf, predicted_weight)
    """
    input_vector = np.array(input_vector).reshape(1, -1)
    rf_est = rf_rf.predict(input_vector)[0]
    weight_est = rf_weight.predict(input_vector)[0]
    return rf_est, weight_est

# --- Example usage (for your given input) ---
#input_vector = [
#    28.02919603, 28.85779898, 28.44662807, 27.43628104, 28.66617122,
#    27.73155523, 24.64874037, 22.95335333, 26.22720405, 24.21180338,
#    6.05329586, 6.49089979, 6.159172323, 5.418504035, 6.144673094,
#    4.442702595, 4.819598924, 5.202283445, 5.247025691, 4.421178302,
#    4.735314264, 4.895437801, 4.935854921, 4.856812295, 5.590097472
#]
#
#rf_est, weight_est = predict_rf_and_weight(input_vector)
#print("Predicted min_nonstrength_rf:", rf_est)
#print("Predicted weight:", weight_est)
