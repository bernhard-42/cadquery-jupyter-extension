from uuid import uuid4
from math import tan, sqrt
import os
import xml.etree.ElementTree as ET

import jinja2
from OCC.Display.WebGl.x3dom_renderer import X3DExporter, ExportEdgeToILS
from OCC.Extend.TopologyUtils import discretize_edge
from cadquery.occ_impl.geom import BoundBox

import cadquery
import cq_jupyter
try:
    import cqparts
    from cqparts.display.material import COLOR
    from cqparts.utils import CoordSystem
    has_cqparts = True
except:
    has_cqparts = False

import IPython

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


# adapted from https://github.com/tpaviot/pythonocc-core/blob/cf83d18dd875c493095b2876468671d07e65af6c/src/Display/WebGl/x3dom_renderer.py#L173
def _indexed_lineset_to_x3d_string(str_linesets, id, color, ils_id=0):
    if color is None:
        color = (1, 0, 0)

    x3dfile_str = "<Switch whichChoice='0' id='swBRP'>\n"
    x3dfile_str += "\t<Group>\n"

    for str_lineset in str_linesets:
        x3dfile_str += "\t\t<Transform scale='1 1 1'><Shape DEF='edg%s'>\n" % id
        x3dfile_str += "\t\t\t<Appearance><Material emissiveColor='%f %f %f'/></Appearance>\n\t\t" % color
        x3dfile_str += str_lineset
        x3dfile_str += "\t\t</Shape></Transform>\n"

    x3dfile_str += "\t</Group>\n"
    x3dfile_str += "</Switch>\n"

    return x3dfile_str

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

    def _to_x3dstr(cadObj):
        if isinstance(cadObj, cq_jupyter.Part):
            part = cadObj
            exporter = X3DExporter(part.compound().wrapped, vertex_shader, fragment_shader, export_edges,
                                part.color, part.color, shininess, transparency, line_color,
                                line_width, mesh_quality)
            exporter.compute()
            x3d_str_shape =  exporter.to_x3dfile_string(part.id)

            root = ET.fromstring(x3d_str_shape)
            scene = root.findall("Scene")[0]
            switches = scene.findall("Switch")
            switches[0].attrib["id"] = "switch_shape%d" % part.id
            switches[1].attrib["id"] = "switch_shape%d_edges" % part.id
            return "\n".join([ET.tostring(s, encoding='utf8', method='html').decode("utf-8") for s in switches])

        elif isinstance(cadObj, cq_jupyter.Assembly):
            assembly = cadObj
            x3d_str = ""
            for cadObj in assembly.parts():
                x3d_str += _to_x3dstr(cadObj)
            return x3d_str
        elif isinstance(cadObj, cq_jupyter.Edges):
            def to_lineset(edge):
                return ExportEdgeToILS(discretize_edge(edge.toOCC()))
            occ_edges = [to_lineset(edge) for edge in cadObj.edges.all()]
            x3d_str_edges = _indexed_lineset_to_x3d_string(occ_edges, id=cadObj.id, color=cadObj.color)
            root = ET.fromstring(x3d_str_edges)
            root.attrib["id"] = "switch_edges%d_edges" % cadObj.id
            return ET.tostring(root, encoding='utf8', method='html').decode("utf-8")
        else:
            print("ERROR")

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
        _to_x3dstr(assembly),
        tree=assembly.to_nav_json(),
        viewpoint_type=viewpoint_type,
        viewpoints=viewpoints,
        center=(c.x, c.y, c.z),
        height=height,
        fov=fov,
        debug=debug)


def convertCqparts(cqpartAssembly, name="root", default_color=None):
    if default_color is None:
        default_color = (255, 255, 0)

    cqpartAssembly.solve()

    parts = []
    for k,v in cqpartAssembly._components.items():
        if isinstance(v, cqparts.Part):
            color = v._render.color
            if isinstance(color, (list, tuple)):
                pass
            elif isinstance(color, str):
                color = COLOR.get(color)
                if color is None:
                    color = default_color
            else:
                color = default_color
            color = tuple((c / 255.0 for c in color))
            parts.append(cq_jupyter.Part(v.world_obj, k, color))
        else:
            parts.append(convertCqparts(v, k, default_color))
    return cq_jupyter.Assembly(name, parts)


def display(cadObj, height=400, ortho=True, fov=0.2, debug=False, default_color=None):
    """
    Jupyter 3D representation support
    """
    if default_color is None:
        default_color = (255, 255, 0)

    def _display(html):
        IPython.display.display(IPython.display.HTML(html))

    if isinstance(cadObj, cadquery.Shape):
        part = cq_jupyter.Part(cadquery.CQ(cadObj), "part", default_color)
        html = x3d_display(cq_jupyter.Assembly("root", [part]),
                           export_edges=True, height=height, ortho=ortho, fov=fov, debug=debug)
        _display(html)

    elif isinstance(cadObj, cadquery.Workplane):
        part = cq_jupyter.Part(cadObj, "part", default_color)
        html = x3d_display(cq_jupyter.Assembly("root", [part]),
                           export_edges=True, height=height, ortho=ortho, fov=fov, debug=debug)
        _display(html)

    elif isinstance(cadObj, cq_jupyter.Assembly):
        html = x3d_display(cadObj,
                           export_edges=True, height=height, ortho=ortho, fov=fov, debug=debug)
        _display(html)

    elif isinstance(cadObj, cq_jupyter.Part):
        html = x3d_display(cq_jupyter.Assembly("root", [cadObj]),
                           export_edges=True, height=height, ortho=ortho, fov=fov, debug=debug)
        _display(html)

    elif has_cqparts and isinstance(cadObj, cqparts.Assembly):
        cadObj.world_coords = CoordSystem()
        assembly = convertCqparts(cadObj)
        display(assembly)
    elif has_cqparts and isinstance(cadObj, cqparts.Part):
        part = cq_jupyter.Part(cadObj.local_obj,"part", default_color)
        display(part)
    else:
        return cadObj
