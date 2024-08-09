import struct

class Texture(object):
    def __init__(self, path):
        self.path = path
        self.load()

    def load(self):
        with open(self.path, "rb") as image:
            image.seek(10)
            header_size = struct.unpack("=l", image.read(4))[0]

            image.seek(18)
            self.width = struct.unpack("=l", image.read(4))[0]
            self.height = struct.unpack("=l", image.read(4))[0]

            image.seek(header_size)

            self.pixels = []

            for y in range(self.height):
                row = []
                for x in range(self.width):
                    b = ord(image.read(1)) / 255
                    g = ord(image.read(1)) / 255
                    r = ord(image.read(1)) / 255
                    row.append((r, g, b))
                self.pixels.append(row)

    def getColor(self, u, v):
        u = max(0, min(1, u))
        v = max(0, min(1, v))

        x = int(u * (self.width - 1))
        y = int(v * (self.height - 1))

        return self.pixels[y][x]
