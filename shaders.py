from MathLib import matrix_vector_mult


def vertexShader(vertex, **kwargs):
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    viewportMatrix = kwargs["viewportMatrix"]

    vt = [vertex[0], vertex[1], vertex[2], 1]

    vt = matrix_vector_mult(viewportMatrix,
            matrix_vector_mult(projectionMatrix,
            matrix_vector_mult(viewMatrix,
            matrix_vector_mult(modelMatrix, vt))))

    if vt[3] != 0:
        vt = [vt[0] / vt[3], vt[1] / vt[3], vt[2] / vt[3], vt[3]]

    return vt



def fragmentShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    texCoords = kwargs["texCoords"]

    tx = texCoords[0][0] * u + texCoords[1][0] * v + texCoords[2][0] * w
    ty = texCoords[0][1] * u + texCoords[1][1] * v + texCoords[2][1] * w

    # Asegúrate de que tx y ty están en el rango [0, 1]
    tx = max(0, min(1, tx))
    ty = max(0, min(1, ty))

    texColor = texture.getColor(tx, ty)

    return texColor if texColor else [1, 1, 1]

