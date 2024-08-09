class Obj(object):
    def __init__(self, filename):
        with open(filename, "r") as file:
            lines = file.read().splitlines()

        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []

        for line in lines:
            line = line.strip()

            if not line or line.startswith('#'):
                continue

            try:
                prefix, value = line.split(maxsplit=1)
            except ValueError:
                continue

            if prefix == "v":
                vert = list(map(float, value.split()))
                self.vertices.append(vert)

            elif prefix == "vt":
                vts = list(map(float, value.split()))
                self.texcoords.append([vts[0], vts[1]])

            elif prefix == "vn":
                norm = list(map(float, value.split()))
                self.normals.append(norm)

            elif prefix == "f":
                face = []
                verts = value.split()
                for vert in verts:
                    face.append(list(map(int, vert.split('/'))))
                self.faces.append(face)
