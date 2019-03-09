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
        raise NotImplementedError("not implemented yet")

    def compound(self):
        raise NotImplementedError("not implemented yet")

    def compounds(self):
        raise NotImplementedError("not implemented yet")

    def to_nav_dict(self):
        raise NotImplementedError("not implemented yet")

    def to_nav_json(self):
        return json.dumps([self.to_nav_dict()], indent=2)

    def web_color(self):
        return "rgba(%d, %d, %d, 0.6)" % tuple([c * 255 for c in self.color])


class Part(CADObject):

    def __init__(self, shape, name, color=None, show_shape=True, show_mesh=True):
        self.name = name
        self.id = self.next_id()
        self.color = (1, 1, 0) if color is None else color
        self.shape = shape
        self._compound = Compound.makeCompound(shape.objects)
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


class Faces(Part):
    
    pass


class Edges(CADObject):

    def __init__(self, edges, name, color=None):
        self.edges = edges
        self.name = name
        self.id = self.next_id()
        self.color = (1, 0, 0) if color is None else color

    def to_nav_dict(self):
        return {
            "type": "edges",
            "name": self.name,
            "id": self.id,
            "x3d_name": "edges%d" % self.id,
            "color": self.web_color(),
            "shape": 3,
            "mesh": 1
        }

    def compounds(self):
        return []

    def compound(self):
        return Compound.makeCompound([])

    def parts(self):
        return [self]


class Assembly(CADObject):

    def __init__(self, name, objects):
        self.name = name
        self.id = self.next_id()
        self.objects = objects

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

    @classmethod
    def reset_id(cls):
        global part_id
        part_id = 0
