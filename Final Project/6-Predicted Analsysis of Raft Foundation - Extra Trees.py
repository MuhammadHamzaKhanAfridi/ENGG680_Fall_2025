# Load the Python Standard and DesignScript Libraries
import sys
import clr
sys.path.append(r'C:\\Users\\Asad\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages')
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN

# Place your code below this line
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Make sure ML libraries are accessible (you already used sys.path.append in Dynamo startup script)
import pandas as pd
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

import warnings
warnings.filterwarnings('ignore')

# ========== Step 1: Read Excel Data ==========
file_path = r"C:\Users\Asad\Downloads\Expanded Analysis of Rafts (1).xlsx"
df = pd.read_excel(file_path)
df.columns = df.columns.str.strip()  # Clean column names
# === Step 2: Select and Engineer Features ===
df['Load_per_Column'] = df['Total Axial load on Column (kN)'] / df['Number of  Columns']
df['Raft_Load_Ratio'] = df['Total Axial load on Column (kN)'] / df['Area Of Raft (m^2)']
df['Column_Density'] = df['Number of  Columns'] / df['Area Of Raft (m^2)']
df['Strength_to_Load_Ratio'] = df["Compressive strength of Concrete Fc' (Mpa)"] / df['Maximum Axial Load on Column in kN']

features = [
    'Column Area (m^2)', 'Area Of Raft (m^2)', 'Total Axial load on Column (kN)',
    "Compressive strength of Concrete Fc' (Mpa)", 'Concrete Unit Weight (kN/m^3)',
    'Subgrade Modulus kN/m/m^2', 'Thickness of Raft (mm)',
    'Load_per_Column', 'Raft_Load_Ratio', 'Column_Density', 'Strength_to_Load_Ratio'
]
X = df[features]
y = df[['Settlement (mm)', 'Punching Shear Value', 'Bearing Pressure (kPa)']]

# === Step 3: Train Model ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
model = MultiOutputRegressor(ExtraTreesRegressor(n_estimators=100, max_depth=10, random_state=42))
model.fit(X_train_scaled, y_train)

# === Step 4: Predict from Dynamo Input (IN[0]) ===
try:
    inputs = IN[0]  # List of 9 values from List.Create

    # Unpack inputs
    num_cols = float(inputs[0])
    raft_area = float(inputs[1])
    col_area = float(inputs[2])
    fc = float(inputs[3])
    unit_weight = float(inputs[4])
    subgrade = float(inputs[5])
    max_axial = float(inputs[6])
    total_axial = float(inputs[7])
    thickness = float(inputs[8])

    # Compute engineered features
    load_per_col = total_axial / num_cols
    raft_load_ratio = total_axial / raft_area
    col_density = num_cols / raft_area
    strength_to_load = fc / max_axial

    input_vector = [
        col_area, raft_area, total_axial, fc, unit_weight,
        subgrade, thickness, load_per_col, raft_load_ratio,
        col_density, strength_to_load
    ]

    input_scaled = scaler.transform([input_vector])
    prediction = model.predict(input_scaled)[0]

    labels = ['Settlement (mm)', 'Punching Shear', 'Bearing Pressure (kPa)']
    prediction_dict = dict(zip(labels, map(float, prediction)))

    # === Step 5: Add R² Metrics for Reference ===
    test_pred = model.predict(X_test_scaled)
    r2_scores = [r2_score(y_test.iloc[:, i], test_pred[:, i]) for i in range(3)]
    metrics = dict(zip(labels, [round(r2, 4) for r2 in r2_scores]))

    OUT = [prediction_dict, metrics]

except Exception as e:
    OUT = [f"Prediction Error: {str(e)}", {}]
