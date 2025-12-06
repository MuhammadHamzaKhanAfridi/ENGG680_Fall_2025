import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager

# Inputs from Dynamo
element = UnwrapElement(IN[0])  # Selected Revit element
material_index = 0  # Index of the material to inspect if the element has multiple materials

# Conversion Factor for Density
kgft3_to_kgm3 = 35.3147

# Get the active document
doc = DocumentManager.Instance.CurrentDBDocument

# Retrieve the material from the selected element
material = None

if isinstance(element, FamilyInstance) or isinstance(element, Wall):
    # Handle specific element types to extract the material
    material_ids = element.GetMaterialIds(False)
    if len(material_ids) > material_index:
        material = doc.GetElement(material_ids[material_index])

if material is not None:
    # Get Structural Asset Id
    structural_asset_id = material.StructuralAssetId
    if structural_asset_id != ElementId.InvalidElementId:
        # Get Structural Asset
        asset_element = doc.GetElement(structural_asset_id)
        structural_asset = asset_element.GetStructuralAsset()
        
        # Extract Density in kg/ft³
        density_kgft3 = structural_asset.Density
        
        # Convert to kg/m³
        density_kgm3 = density_kgft3 * kgft3_to_kgm3
    else:
        density_kgm3 = "No structural asset associated with the material"
else:
    density_kgm3 = "Material not found in the selected element"
#convert kg/m3 to KN/m3
OUT = round(density_kgm3*0.009817,2)
