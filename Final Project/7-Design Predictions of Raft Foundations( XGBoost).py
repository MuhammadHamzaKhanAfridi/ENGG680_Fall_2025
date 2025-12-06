# Load the Python Standard and DesignScript Libraries
import sys
import clr
sys.path.append(r'C:\\Users\\Zain\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages')
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN

# Place your code below this line
# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN

# Place your code below this line
import math
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')

# ------------------ Step 1: Load Excel Data ------------------
file_path = r"C:\Users\Asad\Downloads\Expanded Design data of raft.xlsx"
df = pd.read_excel(file_path)

# ------------------ Step 2: Define Input & Output Features ------------------
X = df[[ 
    'Number of  Columns', 'Area Of Raft (m^2)', "Compressive strength of Concrete Fc' (Mpa)",
    'Concrete Unit Weight (kN/m^3)', 'Subgrade Modulus kN/m/m^2',
    'Column Area (m^2)', 'Maximum Axial Load on Column in kN',
    'Total Axial load on Column (kN)', 'Thickness of Raft (mm)',
    'Preffered Dia of Bars (mm) in Bottom direction X direction',
    'Preffered Dia of Bars (mm) X Top direction',
    'Preffered Dia of Bars (mm) Bottom Y direction',
    'Preffered Dia of Bars (mm) Top Y direction'
]]

y = df[[ 
    'Bottom As (mm^2/m) X strip',
    'Top As (mm^2/m) X strip',
    'Bottom As (mm^2/m) Y strip',
    'Top As (mm^2/m) Y strip'
]]

# ------------------ Step 3: Split and Scale ------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Polynomial Features
poly = PolynomialFeatures(degree=2, include_bias=False)
X_train_poly = poly.fit_transform(X_train_scaled)
X_test_poly = poly.transform(X_test_scaled)

# ------------------ Step 4: Train XGBoost Models ------------------
xgb_params = {
    'max_depth': 4,
    'min_child_weight': 5,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'reg_alpha': 0.1,
    'reg_lambda': 1.0,
    'learning_rate': 0.05,
    'n_estimators': 1000,
    'random_state': 42
}

xgb_models = []
for i in range(y.shape[1]):
    model = xgb.XGBRegressor(**xgb_params, early_stopping_rounds=50)
    model.fit(X_train_poly, y_train.iloc[:, i], eval_set=[(X_test_poly, y_test.iloc[:, i])], verbose=False)
    xgb_models.append(model)

# ------------------ Step 5: Spacing and Count Calculations ------------------
def calculate_bar_spacing_and_count(area_required, bar_diameter, strip_width=1000):
    area_required = max(area_required, 0)
    bar_area = (math.pi * bar_diameter ** 2) / 4

    if bar_area <= 0:
        return 200, 1

    num_bars_per_meter = area_required / bar_area
    if num_bars_per_meter > 0:
        spacing = strip_width / num_bars_per_meter
        spacing = round(spacing / 5) * 5
        num_bars = math.ceil(strip_width / spacing) + 1
    else:
        spacing = strip_width
        num_bars = 1

    min_spacing = max(3 * bar_diameter, 75)
    max_spacing = 200
    spacing = max(min_spacing, min(spacing, max_spacing))
    num_bars = math.ceil(strip_width / spacing) + 1

    return spacing, num_bars

def predict_with_calculations(y_pred_areas, X_original):
    all_predictions = np.zeros((y_pred_areas.shape[0], 12))
    for i in range(y_pred_areas.shape[0]):
        # Extract bar diameters
        bottom_x_dia = X_original[i][9]
        top_x_dia = X_original[i][10]
        bottom_y_dia = X_original[i][11]
        top_y_dia = X_original[i][12]

        current_areas = y_pred_areas[i]
        if len(current_areas.shape) > 1:
            current_areas = current_areas.flatten()
        areas = [max(area, 0) for area in current_areas]
        diameters = [bottom_x_dia, top_x_dia, bottom_y_dia, top_y_dia]

        for j, (area, dia) in enumerate(zip(areas, diameters)):
            spacing, num_bars = calculate_bar_spacing_and_count(area, dia)
            all_predictions[i, j * 3:(j + 1) * 3] = [area, spacing, num_bars]

    return all_predictions.tolist()

# ------------------ Step 6: Dynamo IN Prediction ------------------
dataEnteringNode = IN
input_data = IN[0]  # Expecting [[labels], [values]]
if not input_data or len(input_data) < 2:
    OUT = "Invalid input structure. Expecting [[labels], [values]]"
else:
    try:
        # Convert to numpy
        input_values = np.array([input_data[1]])  # 1 row
        input_scaled = scaler.transform(input_values)
        input_poly = poly.transform(input_scaled)

        # Predict areas
        area_preds = np.array([model.predict(input_poly) for model in xgb_models]).T  # shape: (1, 4)

        # Combine with original X input row to get bar diameters
        final_output = predict_with_calculations(area_preds, [input_data[1]])

        OUT = final_output  # List of [As, spacing, bar_count] × 4 strips

    except Exception as e:
        OUT = "Error during prediction: " + str(e)

