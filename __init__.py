import sys
import importlib
from pathlib import Path


def reload():
    """
    Reload the library
    :return:
    """

    # Modules contain references to other modules, and a freshly reloaded module may use a reference to an old one.
    # Tracking down dependencies properly is hard, so doing it in a dumb way.
    # Sorry.

    for i in range(3):
        for mn, mod in list(sys.modules.items()):
            if __name__ in mn:
                print(mod)
                importlib.reload(mod)

if __name__ == '__main__':
    my_dir = Path(__file__).parent

    print("To enable this module in freecad, run this (once every time you run freecad)")
    print('import sys')
    print('sys.path.append("%s")' % my_dir.parent.absolute())


