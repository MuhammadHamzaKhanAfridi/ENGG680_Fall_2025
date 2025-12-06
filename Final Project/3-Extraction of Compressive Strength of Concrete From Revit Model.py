import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager

# Inputs from Dynamo
element = UnwrapElement(IN[0])  # Selected Revit element
material_index = 0  # Index of the material to inspect if the element has multiple materials


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
        
        Compressive_Strength = structural_asset.ConcreteCompression
        
    else:
        CompressiveStrength = "No structural asset associated with the material"
else:
    CompressiveStrength = "Material not found in the selected element"
# converting N/ft.m Revit's Inbuilt Concrete Compression Unit and rounding to two decimal places
OUT = round(Compressive_Strength/304800,2)