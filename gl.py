import struct
from camera import Camera
from math import tan, pi
from MathLib import barycentricCoords, matrix_vector_mult
from model import Model
from texture import Texture

def char(c):
    return struct.pack("=c", c.encode("ascii"))

def word(w):
    return struct.pack("=h", w)

def dword(d):
    return struct.pack("=l", d)

POINTS = 0
LINES = 1
TRIANGLES = 2

class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.camera = Camera()
        self.glViewport(0, 0, self.width, self.height)
        self.glProjection()
        self.glColor(1, 1, 1)
        self.glClearColor(0, 0, 0)
        self.glClear()
        self.vertexShader = None
        self.fragmentShader = None
        self.primitiveType = TRIANGLES
        self.models = []
        self.textures = []

    def glViewport(self, x, y, width, height):
        self.vpX = int(x)
        self.vpY = int(y)
        self.vpWidth = width
        self.vpHeight = height
        self.viewportMatrix = [
            [width / 2, 0, 0, x + width / 2],
            [0, height / 2, 0, y + height / 2],
            [0, 0, 0.5, 0.5],
            [0, 0, 0, 1]
        ]

    def glProjection(self, n=0.1, f=1000, fov=60):
        aspectRatio = self.vpWidth / self.vpHeight
        fov = fov * pi / 180
        t = tan(fov / 2) * n
        r = t * aspectRatio
        self.projectionMatrix = [
            [n / r, 0, 0, 0],
            [0, n / t, 0, 0],
            [0, 0, -(f + n) / (f - n), -(2 * f * n) / (f - n)],
            [0, 0, -1, 0]
        ]

    def glColor(self, r, g, b):
        self.currColor = [min(1, max(0, r)), min(1, max(0, g)), min(1, max(0, b))]

    def glClearColor(self, r, g, b):
        self.clearColor = [min(1, max(0, r)), min(1, max(0, g)), min(1, max(0, b))]

    def glClear(self):
        color = [int(i * 255) for i in self.clearColor]
        self.screen.fill(color)

    def loadModel(self, modelPath, texturePath):
        model = Model(modelPath)
        model.centerAndScale()
        texture = Texture(texturePath)
        self.models.append(model)
        self.textures.append(texture)

    def glRender(self):
        print("Rendering frame")
        for model, texture in zip(self.models, self.textures):
            modelMatrix = model.GetModelMatrix()
            viewMatrix = self.camera.GetViewMatrix()
            projectionMatrix = self.projectionMatrix

            for face in model.faces:
                verts = [model.vertices[idx[0] - 1] for idx in face]
                texCoords = [model.texcoords[idx[1] - 1] for idx in face]
                transformedVerts = [self.vertexShader(vertex, modelMatrix=modelMatrix, viewMatrix=viewMatrix,
                                                      projectionMatrix=projectionMatrix,
                                                      viewportMatrix=self.viewportMatrix) for vertex in verts]

                if transformedVerts:
                    self.glTriangle(transformedVerts[0], transformedVerts[1], transformedVerts[2], texture, texCoords)

    def glTriangle(self, A, B, C, texture, texCoords):
        # Calcular la caja delimitadora del triángulo
        bboxMin, bboxMax = self.bbox(A, B, C)
        areaABC = (B[0] - A[0]) * (C[1] - A[1]) - (C[0] - A[0]) * (B[1] - A[1])

        if abs(areaABC) < 1e-5:  # Verificar que el triángulo sea válido
            return

        # Bucle sobre cada píxel en la caja delimitadora
        for x in range(max(0, bboxMin[0]), min(self.width, bboxMax[0] + 1)):
            for y in range(max(0, bboxMin[1]), min(self.height, bboxMax[1] + 1)):
                # Calcular las coordenadas baricéntricas
                w = ((B[0] - A[0]) * (y - A[1]) - (B[1] - A[1]) * (x - A[0])) / areaABC
                v = ((C[0] - A[0]) * (y - A[1]) - (C[1] - A[1]) * (x - A[0])) / areaABC
                u = 1 - v - w

                # Comprobar si el punto P está dentro del triángulo
                if u >= 0 and v >= 0 and w >= 0:
                    # Interpolación de coordenadas de textura
                    tx = texCoords[0][0] * u + texCoords[1][0] * v + texCoords[2][0] * w
                    ty = texCoords[0][1] * u + texCoords[1][1] * v + texCoords[2][1] * w

                    # Normalización de las coordenadas de textura
                    tx = max(0, min(1, tx))
                    ty = max(0, min(1, ty))

                    # Fragment Shader para calcular el color
                    kwargs = {
                        "verts": [A, B, C],
                        "bCoords": (u, v, w),
                        "texture": texture,
                        "texCoords": texCoords
                    }
                    color = self.fragmentShader(**kwargs)
                    self.glPoint(x, y, color)

    def bbox(self, *vertices):
        xs = [v[0] for v in vertices]
        ys = [v[1] for v in vertices]
        return [int(min(xs)), int(min(ys))], [int(max(xs)), int(max(ys))]

    def glPoint(self, x, y, color):
        try:
            self.screen.set_at((x, y), [int(c * 255) for c in color])
        except:
            pass

    def glGenerateFrameBuffer(self, filename):
        pass
