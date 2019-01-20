from uuid import uuid4
from math import tan, sqrt
import os
import jinja2
from OCC.Display.WebGl.x3dom_renderer import X3DExporter
from cadquery.occ_impl.geom import BoundBox

from .viewpoint import viewpoint, isometric, top, bottom, front, rear, left, right

N_HEADER_LINES = 11


def add_x3d_boilerplate(src, tree, viewpoint_type, viewpoints, height=400, center=(0, 0, 0), fov=0.1, debug=False):
    id = uuid4()
    print("View id:", id)
    templateLoader = jinja2.FileSystemLoader(searchpath=os.path.dirname(__file__))
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "x3d_template.j2"
    template = templateEnv.get_template(TEMPLATE_FILE)

    html = template.render(
        src=src,
        tree=tree,
        id=id,
        height=height,
        divheight=height + 100,
        viewpoint_type=viewpoint_type,
        viewpoints=viewpoints,
        x0=center[0],
        y0=center[1],
        z0=center[2],
        fov=fov)

    if debug:
        print(html)
    return html


def x3d_display(assembly,
                vertex_shader=None,
                fragment_shader=None,
                export_edges=True,
                specular_color=(1, 1, 1),
                shininess=0.4,
                transparency=0.4,
                line_color=(0, 0, 0),
                line_width=2.,
                mesh_quality=.3,
                ortho=False,
                fov=0.1,
                height=400,
                debug=False):

    x3d_str = ""
    for part in assembly.parts():
        exporter = X3DExporter(part.compound().wrapped, vertex_shader, fragment_shader, export_edges, part.color,
                               part.color, shininess, transparency, line_color, line_width, mesh_quality)

        exporter.compute()

        x3d_str_shape = exporter.to_x3dfile_string(part.id)
        x3d_str += '\n'.join(x3d_str_shape.splitlines()[N_HEADER_LINES:-2]) + "\n"

    compound = assembly.compound().wrapped

    bb = BoundBox._fromTopoDS(compound)
    d = [0.5 * b for b in (bb.xlen, bb.ylen, bb.zlen)]
    c = bb.center

    if ortho:
        viewpoint_type = "OrthoViewpoint"
        dist = sqrt(sum([x * x for x in d]))
        fov = "%f %f %f %f" % (-dist, -dist, dist, dist)
    else:
        viewpoint_type = "Viewpoint"
        tanfov2 = tan(fov / 2.0)
        dist = sqrt(sum([x * x for x in d])) / tanfov2
    viewpoints = {}
    viewpoints["iso"] = viewpoint(*isometric(), c, dist)
    viewpoints["top"] = viewpoint(*top(), c, dist)
    viewpoints["bottom"] = viewpoint(*bottom(), c, dist)
    viewpoints["front"] = viewpoint(*front(), c, dist)
    viewpoints["rear"] = viewpoint(*rear(), c, dist)
    viewpoints["left"] = viewpoint(*left(), c, dist)
    viewpoints["right"] = viewpoint(*right(), c, dist)

    return add_x3d_boilerplate(
        x3d_str,
        tree=assembly.to_nav_json(),
        viewpoint_type=viewpoint_type,
        viewpoints=viewpoints,
        center=(c.x, c.y, c.z),
        height=height,
        fov=fov,
        debug=debug)
