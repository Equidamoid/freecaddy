import Part
import typing
import math
import numpy as np
import freecaddy.refs as fcr
from dataclasses import dataclass
from .abbreviations import *


class Transform:
    def apply(self, shape: Part.Shape, preserve_original=True):
        pass

    def __invert__(self):
        pass


@dataclass(frozen=True)
class Rotation(Transform):
    angle: float
    ref: v = fcr.O
    axis: v = fcr.OZ

    def apply(self, shape: Part.Shape, preserve_original=True):
        if preserve_original:
            shape = shape.copy()
        shape.rotate(self.ref, self.axis, self.angle)
        return shape

    def __invert__(self):
        return Rotation(angle=-self.angle, ref=self.ref, axis=self.axis)


@dataclass(frozen=True)
class Translation(Transform):
    dx: float = 0
    dy: float = 0
    dz: float = 0

    @classmethod
    def spherical(cls, r: float, phi=0.0, theta=0.0):
        assert theta == 0.0, "theta is not implemented yet"
        p = math.radians(phi)
        c = math.cos
        s = math.sin
        return Translation(
            r * c(p),
            r * s(p),
            0
        )
    def apply(self, shape: Part.Shape, preserve_original=True):
        if preserve_original:
            shape = shape.copy()
        shape.translate((self.dx, self.dy, self.dz))
        return shape

    def __invert__(self):
        return Translation(-self.dx, -self.dy, -self.dz)


@dataclass(frozen=True)
class Reflection(Transform):
    ref: v = fcr.O
    axis: v = fcr.OZ

    def apply(self, shape: Part.Shape, preserve_original=True):
        return shape.mirror(self.ref, self.axis)

    def __invert__(self):
        return self


class TransformChain:
    def __init__(self):
        self._transforms: typing.List[Transform] = []

    @property
    def copy(self):
        return self.clone()

    def clone(self):
        ret = TransformChain()
        ret._transforms = list(self._transforms)
        return ret

    def translate(self, dx=0., dy=0., dz=0.):
        self._transforms.append(Translation(dx, dy, dz))
        return self

    def translate_sph(self, r: float, phi=0.0, theta=0.0):
        self._transforms.append(Translation.spherical(r, phi, theta))
        return self

    def rotate(self, ref: v = fcr.O, axis: v = fcr.OZ, angle: float = 0):
        self._transforms.append(Rotation(ref=ref, axis=axis, angle=angle))
        return self

    def mirror(self, ref=fcr.O, axis=fcr.OZ):
        self._transforms.append(Reflection(ref, axis))
        return self

    def chain(self, other: 'TransformChain'):
        self._transforms += other._transforms
        return self

    def __invert__(self):
        ret = id()
        for tr in self._transforms[::-1]:
            ret += ~tr
        return ret

    def inverse(self):
        return ~self

    def __mul__(self, n):
        assert n >= 0
        ret = id()
        for i in range(n):
            ret = ret.chain(self)
        return ret

    def __iadd__(self, other):
        if isinstance(other, Transform):
            self._transforms.append(other)
        elif isinstance(other, TransformChain):
            self._transforms += other._transforms
        else:
            raise NotImplemented
        return self

    def __add__(self, other):
        ret = self.copy
        ret += other
        return ret

    def __call__(self, shape: Part.Shape) -> Part.Shape:
        ret = shape.copy()
        for tr in self._transforms:
            ret = tr.apply(ret, False)
        return ret


def wiggle(shape: Part.Shape, dx=None, dy=None, dz=None) -> typing.Iterable[Part.Shape]:
    """
    A non-isotropic alternative to Part.offset.
    One use case is accounting for FDM tolerances: cartesian FDM printers are much more precise in Y direction than
    in X and Y.
    """
    def to_deltas(x):
        if isinstance(x, (list, tuple)):
            return x
        if x:
            return [x, -x]
        return [0]

    for x in to_deltas(dx):
        for y in to_deltas(dy):
            for z in to_deltas(dz):
                yield TransformChain().translate(x, y, z)(shape)


def ref(shape: Part.Shape, origin=None, direction=None, roll: float = None) -> Part.Shape:
    """
    Applying usual FreeCAD's `point=..., direction=...` to any shape.
    ref(pnt, dir)(Part.makeBox(x, y, z)) is equivalent to Part.makeBox(x, y, z, png, dir),
    but does not require copypasting code when creating your own shapes.

    :param origin: Move the shape to specified origin point from default (0, 0, 0)
    :param direction: Orient the shape so former Z axes points in specified direction
    :param roll: Rotate the shape around it's initial Z axis
    :return: `shape`, the object is modified in place
    """

    if roll is not None:
        shape.rotate(fcr.OZ, roll)

    if direction is not None:
        direction = np.array(list(direction))
        assert len(direction) == 3
        direction /= np.sqrt((direction * direction).sum())
        ax = np.cross(np.array([0, 0, 1]), direction)
        angle = math.degrees(math.sqrt((ax * ax).sum()))
        shape.rotate(fcr.O, v(*ax), angle)

    if origin:
        shape.translate(origin)

    return shape


def translate(dx=0, dy=0, dz=0):
    return TransformChain().translate(dx, dy, dz)


def rotate(ref: v, axis: v, angle: float):
    return TransformChain().rotate(ref, axis, angle)


def id(): return TransformChain()