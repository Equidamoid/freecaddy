import math


class HexGrid:
    def __init__(self, x0, y0, layers, odd_layer_len, clearance):
        self.x0 = x0
        self.y0 = y0
        self.layers = layers
        self.odd_layer_len = odd_layer_len
        self.clearance = clearance
        self.layer_offset = clearance * math.sin(math.radians(60))

        self.xspan = (self.odd_layer_len - 1) * self.clearance
        self.yspan = (self.layers - 1) * self.layer_offset


    def iter(self):
        for l in range(self.layers):
            y = self.y0 + l * self.layer_offset
            x0 = self.x0 + self.clearance / 2 * (l % 2)
            for n in range(self.odd_layer_len - (l % 2)):
                yield x0 + self.clearance * n, y


class RectGrid:
    def __init__(self, x0, y0, layers, layer_len, clearance):
        self.x0 = x0
        self.y0 = y0
        self.layers = layers
        self.layer_len = layer_len
        self.clearance = clearance

        self.xspan = (self.layer_len - 1) * self.clearance
        self.yspan = (self.layers - 1) * self.clearance


    def iter(self):
        for l in range(self.layers):
            y = self.y0 + l * self.clearance
            x0 = self.x0
            for n in range(self.layer_len):
                yield x0 + self.clearance * n, y
