from MathLib import TranslationMatrix, RotationMatrix, matrixMult

class Camera(object):
    def __init__(self):
        self.translate = [0, 0, 0]
        self.rotate = [0, 0, 0]

    def GetViewMatrix(self):
        translateMat = TranslationMatrix(self.translate[0], self.translate[1], self.translate[2])
        rotateMat = RotationMatrix(self.rotate[0], self.rotate[1], self.rotate[2])
        camMatrix = matrixMult(translateMat, rotateMat)
        return inverseMatrix(camMatrix)

def inverseMatrix(m):
    return [
        [m[0][0], m[1][0], m[2][0], -(m[0][0]*m[0][3] + m[1][0]*m[1][3] + m[2][0]*m[2][3])],
        [m[0][1], m[1][1], m[2][1], -(m[0][1]*m[0][3] + m[1][1]*m[1][3] + m[2][1]*m[2][3])],
        [m[0][2], m[1][2], m[2][2], -(m[0][2]*m[0][3] + m[1][2]*m[1][3] + m[2][2]*m[2][3])],
        [0, 0, 0, 1]
    ]
