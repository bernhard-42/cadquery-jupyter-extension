import os
import json

import cadquery as cq
from cadquery import Shape, Compound, CQ

from .display import display

part_id = 0

#
# Create simple Part and Assembly classes
#

class CADObject(object):

    def __init__(self):
        self.color = (0.9, 0.9, 0.9)

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

    def _repr_html_(self):
        display(self)


class Part(CADObject):

    def __init__(self, shape, name="part", color=None, show_faces=True, show_edges=True):
        super().__init__()
        self.name = name
        self.id = self.next_id()
        if color is not None:
            self.color = color
        self.shape = shape
        self._compound = Compound.makeCompound(shape.objects)
        self.show_faces = show_faces
        self.show_edges = show_edges

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
            "shape": int(self.show_faces),
            "mesh": int(self.show_edges)
        }


class Faces(Part):

    def __init__(self, shape, name="faces", color=None, show_faces=True, show_edges=True):
        super().__init__(shape, name, color, show_faces, show_edges)


class Edges(CADObject):

    def __init__(self, edges, name="edges", color=None):
        super().__init__()
        self.edges = edges
        self.name = name
        self._compound = Compound.makeCompound(edges.objects)
        self.id = self.next_id()
        if color is not None:
            self.color = color

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

    def compound(self):
        return self._compound

    def compounds(self):
        return [self._compound]

    def parts(self):
        return [self]


class Assembly(CADObject):

    def __init__(self, objects, name="assembly"):
        super().__init__()
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


def is_edges(cadObj):
    return all([isinstance(obj, cq.occ_impl.shapes.Edge) for obj in cadObj.objects])


def is_faces(cadObj):
    return all([isinstance(obj, cq.occ_impl.shapes.Face) for obj in cadObj.objects])


def convert(cadObj):
    if isinstance(cadObj, (Assembly, Part, Faces, Edges)):
        return cadObj
    elif is_edges(cadObj):
        return Edges(cadObj, color=(1, 0, 0))
    elif is_faces(cadObj):
        return Faces(cadObj, color=(0, 1, 0))
    else:
        return Part(cadObj, color=(0.9, 0.9, 0.9), show_edges=False)


def repr_html(obj):
    """
    Jupyter 3D representation support
    """
    if is_edges(obj):
        cadObj = Edges(obj, name="edges", color=(1, 0, 0))
    elif is_faces(obj):
        cadObj = Faces(obj, name="faces", color=(0, 1, 0))
    else:
        cadObj = obj

    return display(cadObj)
