from obj import Obj
from MathLib import TranslationMatrix, RotationMatrix, ScaleMatrix, matrixMult
from texture import Texture

class Model(object):
    def __init__(self, filename):
        objFile = Obj(filename)
        self.vertices = objFile.vertices
        self.faces = objFile.faces
        self.texcoords = objFile.texcoords
        self.translate = [0, 0, 0]
        self.rotate = [0, 0, 0]
        self.scale = [1, 1, 1]

    def GetModelMatrix(self):
        translateMat = TranslationMatrix(self.translate[0], self.translate[1], self.translate[2])
        rotateMat = RotationMatrix(self.rotate[0], self.rotate[1], self.rotate[2])
        scaleMat = ScaleMatrix(self.scale[0], self.scale[1], self.scale[2])
        return matrixMult(matrixMult(translateMat, rotateMat), scaleMat)

    def centerAndScale(self):
        minX, minY, minZ = [float('inf')] * 3
        maxX, maxY, maxZ = [float('-inf')] * 3

        for vertex in self.vertices:
            minX = min(minX, vertex[0])
            minY = min(minY, vertex[1])
            minZ = min(minZ, vertex[2])
            maxX = max(maxX, vertex[0])
            maxY = max(maxY, vertex[1])
            maxZ = max(maxZ, vertex[2])

        centerX = (minX + maxX) / 2
        centerY = (minY + maxY) / 2
        centerZ = (minZ + maxZ) / 2

        self.translate = [-centerX, -centerY, -centerZ]

        scaleFactor = 2 / max(maxX - minX, maxY - minY, maxZ - minZ)
        self.scale = [scaleFactor] * 3
