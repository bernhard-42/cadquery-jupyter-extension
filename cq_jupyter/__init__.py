from .cq_jupyter import Assembly, Part, Edges, Faces, repr_html, convert
from .display import display
from .export import exportSTL
import cadquery as cq

#
# Monkey patching caqdquery to replace the _repr_html_ code
#


print("Overwriting _repr_html_ of cadquery.Shape and cadQuery.Workplane")
try:
    del cq.Shape._repr_html_
except:
    pass
cq.Workplane._repr_html_ = repr_html
