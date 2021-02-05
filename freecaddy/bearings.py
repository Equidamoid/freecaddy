from dataclasses import dataclass

import Part
from FreeCAD import Base

v = Base.Vector


@dataclass
class BearingDimensions:
    d_in: float
    d_out: float
    h: float
    inner_ring: float = None

    def hole_shape(self, z_clearance, xy_clearance=0):
        """
        Shape of the hole where the bearing is to be inserted.
        FIXME: what's the proper term?
        """
        ret = Part.makeCylinder(self.d_out / 2 + xy_clearance, self.h)
        if z_clearance > 0:
            ret = ret.fuse(Part.makeCylinder(self.d_out / 2 * 0.85 - 0.5, self.h + z_clearance))
        return ret

    def axis_shape(self, z_clearance, xy_clearance=0):
        """
        Axis shape, with indent for proper positioning.
        """

        ret = Part.makeCylinder(self.d_in / 2 - xy_clearance, self.h)
        if z_clearance > 0:
            ring_w = self.inner_ring or self.d_in / 2 * 0.2 + 0.5
            # ret.translate((0, 0, clearance))
            ret = ret.fuse(Part.makeCylinder(self.d_in / 2 + self.inner_ring, z_clearance, v(0, 0, -z_clearance)))
        return ret

