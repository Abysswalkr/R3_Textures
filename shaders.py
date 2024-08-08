def vertexShader(vertex, **kwargs):
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    viewportMatrix = kwargs["viewportMatrix"]

    vt = [vertex[0], vertex[1], vertex[2], 1]

    vt = viewportMatrix @ projectionMatrix @ viewMatrix @ modelMatrix @ vt
    vt = vt.tolist()[0]

    vt = [vt[0] / vt[3], vt[1] / vt[3], vt[2] / vt[3]]

    return vt


def fragmentShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    texCoords = kwargs["texCoords"]

    tx = texCoords[0][0] * u + texCoords[1][0] * v + texCoords[2][0] * w
    ty = texCoords[0][1] * u + texCoords[1][1] * v + texCoords[2][1] * w

    texColor = texture.getColor(tx, ty)

    if texColor:
        return texColor
    else:
        return [1, 1, 1]
