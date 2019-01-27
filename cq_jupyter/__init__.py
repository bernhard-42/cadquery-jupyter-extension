from .cq_jupyter import Assembly, Part
from .display import display
import cadquery

#
# Monkey patching caqdquery to replace the _repr_html_ code
#

def _repr_html_(self):
    """
    Jupyter 3D representation support
    """
    part = Part(cadquery.CQ(self), "part", (1, 1, 0))
    return display(Assembly("assembly", [part]), ortho=True)

print("Overwriting _repr_html_ of cadquery.Shape")
cadquery.Shape._repr_html_ = _repr_html_