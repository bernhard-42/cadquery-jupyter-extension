from .cq_jupyter import Assembly, Part, Edges, Faces
from .display import display
from .export import exportSTL
import cadquery as cq

#
# Monkey patching caqdquery to replace the _repr_html_ code
#

def _repr_html_(self):
    """
    Jupyter 3D representation support
    """
    cqObjs = self.objects
    if all([isinstance(obj, cq.occ_impl.shapes.Edge) for obj in cqObjs]):
        cadObj = Edges(self, "edges")
    elif all([isinstance(obj, cq.occ_impl.shapes.Face) for obj in cqObjs]):
        cadObj = Faces(self, "faces")
    else:
        cadObj = self
    return display(cadObj)


print("Overwriting _repr_html_ of cadquery.Shape and cadQuery.Workplane")
try:
    del cq.Shape._repr_html_
except:
    pass
cq.Workplane._repr_html_ = _repr_html_
