from math import pi, sin, cos, isclose

def barycentricCoords(A, B, C, P):
    areaPCB = abs((P[0] * C[1] + C[0] * B[1] + B[0] * P[1]) -
                  (P[1] * C[0] + C[1] * B[0] + B[1] * P[0]))

    areaACP = abs((A[0] * C[1] + C[0] * P[1] + P[0] * A[1]) -
                  (A[1] * C[0] + C[1] * P[0] + P[1] * A[0]))

    areaABP = abs((A[0] * B[1] + B[0] * P[1] + P[0] * A[1]) -
                  (A[1] * B[0] + B[1] * P[0] + P[1] * A[0]))

    areaABC = abs((A[0] * B[1] + B[0] * C[1] + C[0] * A[1]) -
                  (A[1] * B[0] + B[1] * C[0] + C[1] * A[0]))

    if areaABC == 0:
        return None

    u = areaPCB / areaABC
    v = areaACP / areaABC
    w = areaABP / areaABC

    if 0 <= u <= 1 and 0 <= v <= 1 and 0 <= w <= 1 and isclose(u + v + w, 1.0):
        return (u, v, w)
    else:
        return None

def TranslationMatrix(x, y, z):
    return [
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ]

def ScaleMatrix(x, y, z):
    return [
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1]
    ]

def RotationMatrix(pitch, yaw, roll):
    pitch = pitch * pi / 180
    yaw = yaw * pi / 180
    roll = roll * pi / 180

    pitchMat = [
        [1, 0, 0, 0],
        [0, cos(pitch), -sin(pitch), 0],
        [0, sin(pitch), cos(pitch), 0],
        [0, 0, 0, 1]
    ]

    yawMat = [
        [cos(yaw), 0, sin(yaw), 0],
        [0, 1, 0, 0],
        [-sin(yaw), 0, cos(yaw), 0],
        [0, 0, 0, 1]
    ]

    rollMat = [
        [cos(roll), -sin(roll), 0, 0],
        [sin(roll), cos(roll), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]

    return matrixMult(matrixMult(pitchMat, yawMat), rollMat)

def matrixMult(A, B):
    result = [[sum(a * b for a, b in zip(A_row, B_col)) for B_col in zip(*B)] for A_row in A]
    return result

def matrix_vector_mult(matrix, vector):
    result = [0, 0, 0, 0]
    for i in range(4):
        result[i] = (matrix[i][0] * vector[0] +
                     matrix[i][1] * vector[1] +
                     matrix[i][2] * vector[2] +
                     matrix[i][3] * vector[3])
    return result
