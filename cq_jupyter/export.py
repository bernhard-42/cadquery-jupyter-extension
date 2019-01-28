import cadquery
from cadquery import Compound
from .display import convertCqparts
import cq_jupyter
try:
    import cqparts
    from cqparts.display.material import COLOR
    has_cqparts = True
except:
    has_cqparts = False

def exportSTL(cadObj, filename, precision=0.001):
    compound = None
    if isinstance(cadObj, cadquery.Shape):
        compound = Compound.makeCompound(cadObj.objects)
    elif isinstance(cadObj, cadquery.Workplane):
        compound = Compound.makeCompound(cadObj.objects)
    elif isinstance(cadObj, cq_jupyter.Assembly):
        compound = cadObj.compound()
    elif isinstance(cadObj, cq_jupyter.Part):
        compound = cadObj.compound()
    elif has_cqparts and isinstance(cadObj, cqparts.Assembly):
        assembly = convertCqparts(cadObj)
        exportSTL(assembly, filename, precision)
    elif has_cqparts and isinstance(cadObj, cqparts.Part):
        part = cq_jupyter.Part(cadObj.local_obj, "part")
        exportSTL(part, filename)
    else:
        print("Unknown CAD object", type(cadObj))

    if compound is not None:
        compound.exportStl(filename, precision=precision)   
    
