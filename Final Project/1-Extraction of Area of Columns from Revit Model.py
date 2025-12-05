# Load the Python Standard and DesignScript Libraries
import sys
# For Dynamo CPython3 or pyRevit
import clr
import sys

# Add Revit API references
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument

def get_top_face_area(column):
    options = Options()
    options.ComputeReferences = True
    options.IncludeNonVisibleObjects = False

    geometry_element = column.get_Geometry(options)

    for geo in geometry_element:
        if isinstance(geo, Solid) and geo.Faces.Size > 0:
            top_face = None
            max_z = -1e6

            for face in geo.Faces:
                try:
                    # Get mid-UV and normal
                    bbox = face.GetBoundingBox()
                    u = (bbox.Min.U + bbox.Max.U) / 2
                    v = (bbox.Min.V + bbox.Max.V) / 2
                    uv = UV(u, v)
                    normal = face.ComputeNormal(uv)

                    # Check if normal points upward (Z axis)
                    if normal.Z > 0.99:
                        # Triangulate and get average Z
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

# Collect all structural columns
collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralColumns).WhereElementIsNotElementType().ToElements()

areas = []

for column in collector:
    area = get_top_face_area(column)
    areas.append(area*0.092903)

# Output in Dynamo (use OUT)
OUT = areas
