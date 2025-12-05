# Automated Design Analysis and Predictive Modeling of Raft Foundations

## Overview

This project implements an automated design analysis and predictive modeling system for raft foundations using machine learning algorithms integrated with Autodesk Dynamo and Revit. The system combines structural engineering principles with advanced ML models to predict settlement, punching shear, bearing pressure, and optimal reinforcement design for raft foundations.

## 🏗️ Project Architecture

The system consists of multiple interconnected components:

1. **Data Extraction from Revit Models** - Automated extraction of structural parameters
2. **Machine Learning Prediction Models** - XGBoost and Extra Trees models for design prediction
3. **Design Compliance Checking** - Automated code compliance verification
4. **Reinforcement Design** - Optimal bar spacing and area calculations

## 📋 Features

### Core Capabilities
- **Automated Parameter Extraction**: Extracts geometric and material properties directly from Revit models
- **ML-Based Predictions**: Uses trained XGBoost and Extra Trees models for accurate predictions
- **Design Compliance**: Automated checking against structural design codes
- **Reinforcement Design**: Calculates optimal reinforcement areas, spacing, and bar counts
- **Real-time Analysis**: Provides instant feedback on design feasibility

### Prediction Outputs
- Settlement analysis (mm)
- Punching shear calculations
- Bearing pressure analysis (kPa)
- Reinforcement design (areas, spacing, bar counts)

## 🔧 Technical Stack

### Software Requirements
- **Autodesk Revit** (2020 or later)
- **Dynamo** (2.0 or later)
- **Python 3.9+**

### Python Dependencies
```
pandas
numpy
scikit-learn
xgboost
openpyxl
math
warnings
```

### Machine Learning Models
- **XGBoost Regressor**: For reinforcement area predictions
- **Extra Trees Regressor**: For settlement, punching shear, and bearing pressure analysis

## 📁 Project Structure

```
raft-foundation-ml/
├── scripts/
│   ├── Code_Compliance_Check.py
│   ├── Design_Predictions_XGBoost.py
│   ├── Extracting_Area_Columns.py
│   ├── Extracting_Area_Slabs.py
│   ├── Extracting_Compressive_Strength.py
│   ├── Extracting_Length_Raft.py
│   ├── Extracting_Unit_Weight.py
│   └── Predicted_Analysis_ExtraTrees.py
├── data/
│   ├── Expanded_Design_data_of_raft.xlsx
│   └── Expanded_Analysis_of_Rafts.xlsx
├── dynamo/
│   └── Raft_Foundation_Analysis.dyn
└── README.md
```

## 🚀 Installation & Setup

### 1. Environment Setup
```bash
# Install required Python packages
pip install pandas numpy scikit-learn xgboost openpyxl
```

### 2. File Path Configuration
Update the following file paths in the scripts:
- `Design_Predictions_XGBoost.py`: Line 28
- `Predicted_Analysis_ExtraTrees.py`: Line 25

```python
# Update these paths to your local directories
file_path = r"C:\Your\Path\To\Expanded Design data of raft.xlsx"
```

### 3. Python Environment Path
Update the Python path in Dynamo scripts:
```python
sys.path.append(r'C:\Users\YourUser\AppData\Local\Programs\Python\Python39\lib\site-packages')
```

### 4. Dynamo Setup
1. Open Dynamo in Revit
2. Load the provided Dynamo script
3. Ensure all Python script nodes are properly configured

## 📊 Data Requirements

### Input Parameters
The system requires the following input parameters:

| Parameter | Unit | Description |
|-----------|------|-------------|
| Number of Columns | - | Total number of structural columns |
| Area of Raft | m² | Total area of the raft foundation |
| Column Area | m² | Cross-sectional area of columns |
| Concrete Compressive Strength | MPa | f'c value |
| Concrete Unit Weight | kN/m³ | Density of concrete |
| Subgrade Modulus | kN/m/m² | Soil subgrade reaction modulus |
| Maximum Axial Load | kN | Maximum load on any column |
| Total Axial Load | kN | Sum of all column loads |
| Raft Thickness | mm | Thickness of raft slab |
| Bar Diameters | mm | Reinforcement bar diameters |

### Training Data
The models are trained on comprehensive datasets containing:
- 1000+ raft foundation design cases
- Various soil conditions and loading scenarios
- Different geometric configurations
- Multiple concrete grades and reinforcement patterns

## 🔍 Component Details

### 1. Data Extraction Scripts

#### `Extracting_Area_Columns.py`
- Extracts column cross-sectional areas from Revit model
- Calculates top face area using geometric analysis
- Converts units from ft² to m²

#### `Extracting_Area_Slabs.py`
- Extracts raft foundation area from floor elements
- Identifies top faces using normal vector analysis
- Provides area basis for design calculations

#### `Extracting_Compressive_Strength.py`
- Retrieves concrete compressive strength from material properties
- Accesses Revit structural asset database
- Converts units from psi to MPa

#### `Extracting_Unit_Weight.py`
- Extracts concrete unit weight from material properties
- Converts from kg/ft³ to kN/m³
- Essential for load calculations

#### `Extracting_Length_Raft.py`
- Calculates equivalent length from raft area
- Rounds to nearest practical dimension
- Used for geometric analysis

### 2. Machine Learning Models

#### `Design_Predictions_XGBoost.py`
Implements XGBoost regression for:
- Bottom reinforcement area (X & Y directions)
- Top reinforcement area (X & Y directions)
- Bar spacing calculations
- Bar count optimization

**Model Parameters:**
```python
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
```

#### `Predicted_Analysis_ExtraTrees.py`
Implements Extra Trees regression for:
- Settlement prediction
- Punching shear analysis
- Bearing pressure calculation

**Feature Engineering:**
- Load per column ratio
- Raft load ratio
- Column density
- Strength to load ratio

### 3. Design Compliance

#### `Code_Compliance_Check.py`
Performs automated compliance checking:
- Settlement limits verification
- Punching shear capacity check
- Bearing pressure validation
- Generates pass/fail reports

**Compliance Criteria:**
- Settlement < Allowable limit (typically 50mm)
- Punching shear ratio < 1.0
- Bearing pressure < Bearing capacity

## 📈 Model Performance

### XGBoost Model (Reinforcement Design)
- **Training Accuracy**: R² > 0.95
- **Cross-validation**: 5-fold CV with R² > 0.92
- **Features**: 13 input parameters + engineered features

### Extra Trees Model (Structural Analysis)
- **Settlement Prediction**: R² > 0.94
- **Punching Shear**: R² > 0.91
- **Bearing Pressure**: R² > 0.93

## 🎯 Usage Guide

### 1. Basic Workflow
1. Open Revit model with structural elements
2. Launch Dynamo and load the script
3. Select structural elements (columns, slabs)
4. Input design parameters
5. Run analysis and review results

### 2. Input Preparation
- Ensure all structural elements are properly modeled
- Verify material properties are assigned
- Check that geometric parameters are realistic

### 3. Results Interpretation
- **Green checkmarks (✅)**: Design passes compliance
- **Red X marks (❌)**: Design failures with specific reasons
- **Numerical outputs**: Predicted values with confidence intervals

### 4. Design Optimization
- Adjust raft thickness for settlement control
- Modify reinforcement based on predictions
- Iterate design parameters for optimal solution

## ⚠️ Limitations & Considerations

### Model Limitations
- Trained on specific design scenarios and codes
- Limited to rectangular raft foundations
- Assumes uniform soil conditions
- Does not account for dynamic loading

### Usage Constraints
- Requires accurate Revit model geometry
- Material properties must be properly defined
- Soil parameters need site-specific data
- Results should be verified by qualified engineers

### Validation Requirements
- Cross-check with traditional design methods
- Verify against local building codes
- Consider site-specific conditions
- Perform sensitivity analysis

## 🔧 Troubleshooting

### Common Issues

#### Script Errors
- **File path issues**: Verify Excel file locations
- **Python path errors**: Update sys.path.append() statements
- **Missing libraries**: Install required packages

#### Model Prediction Issues
- **Invalid inputs**: Check parameter ranges
- **Geometry errors**: Verify Revit model integrity
- **Unit conversions**: Ensure consistent units

#### Dynamo Integration
- **Node failures**: Check Python script syntax
- **Connection errors**: Verify node connections
- **Input/output mismatches**: Check data types

### Debug Steps
1. Check Python console for error messages
2. Verify input parameter ranges
3. Test with known working examples
4. Validate Revit model geometry

## 📝 Future Enhancements

### Planned Features
- Integration with more ML algorithms (Neural Networks, Random Forest)
- Support for irregular raft geometries
- Dynamic loading analysis
- Seismic design considerations
- Cost optimization algorithms

### Model Improvements
- Expanded training datasets
- Multi-objective optimization
- Uncertainty quantification
- Real-time model updates

### User Interface
- GUI development for easier interaction
- Visualization of results
- Report generation capabilities
- Cloud-based deployment

## 🤝 Contributing

### Development Guidelines
1. Follow Python PEP 8 style guidelines
2. Add comprehensive docstrings
3. Include unit tests for new features
4. Update documentation

### Testing Protocol
- Test with various Revit models
- Validate against hand calculations
- Check edge cases and boundary conditions
- Verify cross-platform compatibility


## 🙏 Acknowledgments

- Autodesk for Dynamo and Revit API
- Scikit-learn and XGBoost development teams
- Structural engineering research community
- Open-source Python ecosystem

## 📞 Support

For technical support and questions:
- Contact the  team
- Refer to Autodesk Dynamo documentation
- Check Python ML library documentation

---

**Note**: This tool is intended to assist in preliminary design analysis. All results should be verified by qualified structural engineers and comply with local building codes and standards.