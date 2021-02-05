import Part


def shape_reduce(method: str, shape: Part.Shape, other):
    while other:
        print(other)
        shape = getattr(shape, method)(other[0])
        other = other[1:]
    return shape


def diff(shape: Part.Shape, *holes: Part.Shape) -> Part.Shape:
    return shape_reduce('cut', shape, holes)


def union(shape: Part.Shape, *others: Part.Shape) -> Part.Shape:
    return shape_reduce('fuse', shape, others)


def intersect(shape: Part.Shape, *others: Part.Shape) -> Part.Shape:
    return shape_reduce('common', shape, others)
