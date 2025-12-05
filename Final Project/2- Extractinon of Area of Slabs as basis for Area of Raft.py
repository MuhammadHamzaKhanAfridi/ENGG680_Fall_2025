# Load the Python Standard and Revit Libraries
import clr
import math

clr.AddReference("RevitAPI")
clr.AddReference("RevitServices")

from RevitServices.Persistence import DocumentManager
from Autodesk.Revit.DB import *

# Get the current Revit document
doc = DocumentManager.Instance.CurrentDBDocument

def get_top_face_area(floor):
    options = Options()
    options.ComputeReferences = True
    options.IncludeNonVisibleObjects = False

    geometry_element = floor.get_Geometry(options)

    for geo in geometry_element:
        if isinstance(geo, Solid) and geo.Faces.Size > 0:
            top_face = None
            max_z = -1e6

            for face in geo.Faces:
                try:
                    # Get UV midpoint and compute normal
                    bbox = face.GetBoundingBox()
                    u = (bbox.Min.U + bbox.Max.U) / 2
                    v = (bbox.Min.V + bbox.Max.V) / 2
                    uv = UV(u, v)
                    normal = face.ComputeNormal(uv)

                    # Check for upward facing face
                    if normal.Z > 0.99:
                        # Compute average Z height of triangulated mesh
                        mesh = face.Triangulate()
                        z_sum = 0
                        for i in range(mesh.NumTriangles):
                            tri = mesh.get_Triangle(i)
                            for j in range(3):
                                z_sum += tri.get_Vertex(j).Z
                        avg_z = z_sum / (mesh.NumTriangles * 3)

                        if avg_z > max_z:
                            max_z = avg_z
                            top_face = face
                except:
                    continue

            if top_face:
                return top_face.Area
            else:
                return None
    return None

# Collect all floor elements
floors = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Floors).WhereElementIsNotElementType().ToElements()

# Get the first floor element only
first_floor = floors[0] if len(floors) > 0 else None

if first_floor:
    area_ft2 = get_top_face_area(first_floor)  # Area in ft²
    if area_ft2:
        length_ft = math.sqrt(area_ft2)        # Convert area to length in ft
        length_mm = length_ft * 304.8           # Convert ft to mm
        rounded_mm = round(length_mm, 2)        # Round to 2 decimal places
        OUT = rounded_mm
    else:
        OUT = "No top face area found"
else:
    OUT = "No floors found"
