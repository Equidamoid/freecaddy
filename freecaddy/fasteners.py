import Part
from FreeCAD import Base
import freecaddy.refs as fcr
import freecaddy.shapes as fcs
import math
v = Base.Vector


def hex(width):

    r = width / math.cos(math.pi / 6) / 2
    hexbld = fcs.PolyBuilder([r, 0, 0])
    for i in range(1, 6):
        hexbld.goto_sph(r, 60 * i)
    return hexbld


def bolt_hole(bolt_d, bolt_l, shear_offset, head_d, head_space, nut_hex_w=None, nut_offset=None, nut_h=None):
    """
    Make a template for a bolt hole. The bolt is positioned along the Z axis in negative direction.
    Z=0 corresponds to the shear line
    """
    loose_r = bolt_d * 1.2 / 2 + 0.1
    assert loose_r < head_d / 2
    bottom_l = bolt_l - shear_offset
    ret = Part.makeCylinder(bolt_d / 2 if nut_hex_w is None else loose_r, bottom_l, fcr.O, v(0, 0, -1))
    ret = ret.fuse(Part.makeCylinder(loose_r, bolt_l - bottom_l))
    ret = ret.fuse(Part.makeCylinder(head_d / 2, head_space, v(0, 0, bolt_l - bottom_l)))
    if nut_hex_w:
        r = nut_hex_w / math.cos(math.pi / 6) / 2
        hexbld = fcs.PolyBuilder([r, 0, 0])
        for i in range(1, 6):
            hexbld.goto_sph(r, 60 * i)
        nut = hexbld.face.extrude(v(0, 0, nut_h))
        nut.translate(v(0, 0, -nut_offset - bottom_l))
        # Part.show(nut)
        ret = ret.fuse(nut)

    return ret

