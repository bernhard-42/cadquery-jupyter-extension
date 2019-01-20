from OCC.gp import gp_Quaternion, gp_Vec
from math import atan, sqrt, pi


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
        q = q2 * q1
    axis = gp_Vec(0.0, 0.0, 0.0)
    angle = gp_Quaternion.GetVectorAndAngle(q, axis)
    return (axis, angle)


def isometric():
    return axisAndAngle((1, 0, 0), atan(1 / sqrt(2)), (0, 0, 1), pi / 4)


def front():
    return axisAndAngle((1, 0, 0), pi / 2, (1, 0, 0), pi / 2, True)


def rear():
    return axisAndAngle((1, 0, 0), pi / 2, (0, 0, 1), pi)


def left():
    return axisAndAngle((1, 0, 0), pi / 2, (0, 0, 1), pi / 2)


def right():
    return axisAndAngle((1, 0, 0), pi / 2, (0, 0, 1), -pi / 2)


def top():
    return axisAndAngle((1, 0, 0), pi / 2, (1, 0, 0), -pi / 2)


def bottom():
    return axisAndAngle((1, 0, 0), pi / 2, (1, 0, 0), pi / 2)


def viewpoint(axis, angle, center, dist):
    q = gp_Quaternion(axis, angle)
    viewDir = q.Multiply(gp_Vec(0, 0, 1))
    viewpoint = center.wrapped + (viewDir * dist)
    return {"viewpoint": gp_Vec2list(viewpoint), "axis": gp_Vec2list(axis), "angle": angle}
