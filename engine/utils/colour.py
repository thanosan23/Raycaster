# Colour represented by single 32-bit integer rather than 3 32-bit integers
class Colour:
    def __init__(self, r, g, b):
        self.colour = self.set_colour(r, g, b)
    def set_colour(self, r, g, b):
        ret = 0
        ret <<= 8
        ret |= r
        ret <<= 8
        ret |= g
        ret <<= 8
        ret |= b
        return ret
    def read_colour(self):
        rgb = [0, 0, 0]
        colour = self.colour
        for c in range(3):
            for i in range(8):
                rgb[c] |= ((colour >> i) & 1) << i
            colour >>= 8
        return tuple(reversed(rgb))
    def darken(self):
        self.colour = (self.colour >> 1) & 0x7f7f7f
