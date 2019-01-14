import cadquery as cq
from OCC.Display.WebGl.x3dom_renderer import X3DExporter
from OCC.gp import gp_Quaternion, gp_Vec
from uuid import uuid4
from math import tan, atan, sqrt, pi
import os
import json
import jinja2

from cadquery.occ_impl.geom import BoundBox
from cadquery import Shape, Compound

N_HEADER_LINES = 11

def _gp_Vec_repr(self):
    return "gp_Vec(%f, %f, %f)" % (self.X(), self.Y(), self.Z())

def _gp_Quaternion_repr(self):
    return "gp_Quaternion(%f, %f, %f, %f)" % (self.X(), self.Y(), self.Z(), self.W())

def gp_Vec2list(vec):
    return [vec.X(), vec.Y(), vec.Z()]

gp_Vec.__repr__ = _gp_Vec_repr
gp_Quaternion.__repr__ = _gp_Quaternion_repr


def axisAndAngle(vec1, alpha1, vec2, alpha2, front=False):
    q1 = gp_Quaternion(gp_Vec(*vec1), alpha1)
    if front:
        q = q1
    else:
        q2 = gp_Quaternion(gp_Vec(*vec2), alpha2)
        q = q2*q1
    axis = gp_Vec(0.0, 0.0, 0.0)
    angle = gp_Quaternion.GetVectorAndAngle(q, axis)
    return (axis, angle)

def isometric():
    return axisAndAngle((1,0,0), atan(1/sqrt(2)), (0,0,1), pi/4)

def front():
    return axisAndAngle((1,0,0), pi/2, (1,0,0), pi/2, True)

def rear():
    return axisAndAngle((1,0,0), pi/2, (0,0,1), pi)

def left():
    return axisAndAngle((1,0,0), pi/2, (0,0,1), pi/2)

def right():
    return axisAndAngle((1,0,0), pi/2, (0,0,1), -pi/2)

def top():
    return axisAndAngle((1,0,0), pi/2, (1,0,0), -pi/2)

def bottom():
    return axisAndAngle((1,0,0), pi/2, (1,0,0), pi/2)

def viewpoint(axis, angle, center, dist):
    q = gp_Quaternion(axis, angle)
    viewDir = q.Multiply(gp_Vec(0,0,1))
    viewpoint = center.wrapped + (viewDir * dist)
    return {"viewpoint": gp_Vec2list(viewpoint), "axis": gp_Vec2list(axis), "angle": angle}

def add_x3d_boilerplate(src, parts, viewpoint_type, viewpoints, height=400, center=(0,0,0), fov=0.1, debug=False):
    id = uuid4()
    print("View id:", id)

    templateLoader = jinja2.FileSystemLoader(searchpath=os.path.dirname(__file__))
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "x3d_template.j2"
    template = templateEnv.get_template(TEMPLATE_FILE)    

    html = template.render(src=src,
                           parts=parts,
                           id=id,
                           height=height, divheight=height+100,
                           viewpoint_type=viewpoint_type,
                           viewpoints=viewpoints,
                           x0=center[0], y0=center[1], z0=center[2],
                           fov=fov)

    if debug:
        print(html)
    return html

def x3d_display(*parts,
                vertex_shader=None,
                fragment_shader=None,
                export_edges=True,
                specular_color=(1,1,1),
                shininess=0.4,
                transparency=0.4,
                line_color=(0,0,0),
                line_width=2.,
                mesh_quality=.3,
                ortho=False,
                fov=0.1,
                height=400,
                debug=False):

        x3d_str = ""
        for i, part in enumerate(parts):
            exporter = X3DExporter(part.shape.wrapped,
                                   vertex_shader,
                                   fragment_shader,
                                   export_edges,
                                   part.color,
                                   part.color,
                                   shininess,
                                   transparency,
                                   line_color,
                                   line_width,
                                   mesh_quality)

            exporter.compute()
            x3d_str_shape = exporter.to_x3dfile_string(i)
            x3d_str += '\n'.join(x3d_str_shape.splitlines()[N_HEADER_LINES:-2]) +"\n"

        compound = Compound.makeCompound([part.shape for part in parts]).wrapped
        
        bb = BoundBox._fromTopoDS(compound)
        d = [0.5*b for b in (bb.xlen, bb.ylen, bb.zlen)]
        c = bb.center
        
        if ortho:
            viewpoint_type = "OrthoViewpoint"
            dist = sqrt(sum([x*x for x in d]))
            fov = "%f %f %f %f" % (-dist, -dist, dist, dist)
        else:
            viewpoint_type = "Viewpoint"
            tanfov2 = tan(fov / 2.0)
            dist = sqrt(sum([x*x for x in d])) / tanfov2
        viewpoints = {}
        viewpoints["iso"] = viewpoint(*isometric(),c, dist)
        viewpoints["top"] = viewpoint(*top(), c, dist)
        viewpoints["bottom"] = viewpoint(*bottom(), c, dist)
        viewpoints["front"] = viewpoint(*front(), c, dist)
        viewpoints["rear"] = viewpoint(*rear(), c, dist)
        viewpoints["left"] = viewpoint(*left(), c, dist)
        viewpoints["right"] = viewpoint(*right(), c, dist)

        return add_x3d_boilerplate(x3d_str,
                                   {part.name:{
                                        "name": "shape%d"%i, 
                                        "color": part.web_color(),
                                        "visible": part.visible
                                        } 
                                        for i, part in enumerate(parts)},
                                   viewpoint_type=viewpoint_type,
                                   viewpoints=viewpoints,
                                   center=(c.x,c.y,c.z),
                                   height=height,
                                   fov=fov,
                                   debug=debug)

#
# Create simple Part and Assembly classes
#

class Part(object):
    def __init__(self, shape, name, color=None, visible=True):
        if color is None:
            color = (1,1,0)
        self.shape = shape
        self.name = name
        self.color = color
        self.visible = visible
    
    def web_color(self):
        return "rgba(%d, %d, %d, 0.6)" % tuple([c*255 for c in self.color])
        
class Assembly(object):
    def __init__(self, *parts, ortho=True, fov=0.1, height=400, x=1, debug=False):
        self.parts = parts
        self.height = height
        self.fov = fov
        self.debug = debug
        self.ortho = ortho

    def _repr_html_(self):
        assembly = []
        for part in self.parts:
            # Replace original shape with compound
            assembly.append(Part(Compound.makeCompound(part.shape.objects), part.name, part.color, part.visible))
        
        return x3d_display(*assembly, 
                           export_edges=True, 
                           height=self.height, 
                           ortho=self.ortho, 
                           fov=self.fov,
                           debug=self.debug)

#
# Monkey patching caqdquery to replace the _repr_html_ code
#
def _repr_html_(self):
    """
    Jupyter 3D representation support
    """
    return x3d_display(Part(self, "shape0", (1, 1, 0)), export_edges=True)

Shape._repr_html_ = _repr_html_
