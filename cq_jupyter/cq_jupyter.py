import os
import json

import cadquery as cq
from cadquery import Shape, Compound, CQ

from .display import x3d_display

part_id = 0

#
# Create simple Part and Assembly classes
#

class CADObject(object):

    def next_id(self):
        global part_id
        part_id += 1
        return part_id

    def parts(self):
        raise ("not implemented yet")

    def compound(self):
        raise ("not implemented yet")

    def compounds(self):
        raise ("not implemented yet")

    def to_nav_dict(self):
        raise ("not implemented yet")

    def to_nav_json(self):
        return json.dumps([self.to_nav_dict()], indent=2)


class Part(CADObject):

    def __init__(self, shape, name, color=None, show_shape=True, show_mesh=True):
        self.name = name
        self.id = self.next_id()
        if color is None:
            color = (1, 1, 0)
        self.shape = shape
        self._compound = Compound.makeCompound(shape.objects)
        self.color = color
        self.show_shape = show_shape
        self.show_mesh = show_mesh

    def parts(self):
        return [self]

    def compound(self):
        return self._compound

    def compounds(self):
        return [self._compound]

    def to_nav_dict(self):
        return {
            "type": "part",
            "name": self.name,
            "id": self.id,
            "x3d_name": "shape%d" % self.id,
            "color": self.web_color(),
            "shape": int(self.show_shape),
            "mesh": int(self.show_mesh)
        }

    def web_color(self):
        return "rgba(%d, %d, %d, 0.6)" % tuple([c * 255 for c in self.color])

    def _repr_html_(self):
        return x3d_display(Assembly("assembly", [self]), ortho=True)

class Assembly(CADObject):

    def __init__(self, name, objects, ortho=True, fov=0.1, height=400, debug=False):
        self.name = name
        self.id = self.next_id()
        self.objects = objects
        self.height = height
        self.fov = fov
        self.debug = debug
        self.ortho = ortho

    def parts(self):
        result = []
        for obj in self.objects:
            result += obj.parts()
        return result

    def compounds(self):
        result = []
        for obj in self.objects:
            result += obj.compounds()
        return result

    def compound(self):
        return Compound.makeCompound(self.compounds())

    def to_nav_dict(self):
        return {
            "type": "assembly",
            "name": self.name,
            "id": self.id,
            "shape": 1,
            "mesh": 1,
            "children": [obj.to_nav_dict() for obj in self.objects]
        }

    def _repr_html_(self):
        return x3d_display(
            self, export_edges=True, height=self.height, ortho=self.ortho, fov=self.fov, debug=self.debug)

    @classmethod
    def reset_id(cls):
        global part_id
        part_id = 0


#
# Monkey patching caqdquery to replace the _repr_html_ code
#

def _repr_html_(self):
    """
    Jupyter 3D representation support
    """
    part = Part(CQ(self), "part", (1, 1, 0))
    return x3d_display(Assembly("assembly", [part]), ortho=True)

print("Integrating notebook extension into cadquery.Shape")
Shape._repr_html_ = _repr_html_
