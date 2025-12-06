# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# --- Inputs ---
prediction_dict = IN[0]  # This should be the dictionary: {"Settlement (mm)": ..., ...}
allowable_settlement = IN[1]  # e.g. 50
subgrade_modulus = IN[2]      # e.g. 25000

# --- Extract predictions from dictionary ---
try:
    settlement = prediction_dict["Settlement (mm)"]
    punching = prediction_dict["Punching Shear"]
    bearing_pressure = prediction_dict["Bearing Pressure (kPa)"]

    # --- Bearing capacity formula ---
    bearing_capacity = (subgrade_modulus * settlement) / 2  # in kPa

    # --- Design checks ---
    errors = []

    if settlement > allowable_settlement:
        errors.append("❌ Settlement exceeded: {:.2f} mm > {:.2f} mm".format(settlement, allowable_settlement))

    if punching > 1.0:
        errors.append("❌ Punching shear exceeded: {:.2f} > 1.0".format(punching))

    if bearing_pressure > bearing_capacity:
        errors.append("❌ Bearing pressure exceeded: {:.2f} kPa > Capacity {:.2f} kPa".format(
            bearing_pressure, bearing_capacity))

    # --- Output result ---
    if errors:
        OUT = ["❌ Design Failed", errors]
    else:
        OUT = ["✅ Design Passed", prediction_dict]

except Exception as e:
    OUT = ["❌ Error processing input:", str(e)]
