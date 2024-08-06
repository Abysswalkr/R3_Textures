
def vertexShader(vertex, **kwargs):
    # Se lleva a cabo por cada vertice
    
    # Recibimos las matrices
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    viewportMatrix = kwargs["viewportMatrix"]
    
    # Agregamos un componente W al vertice
    vt = [vertex[0],
          vertex[1],
          vertex[2],
          1]
    
    # Transformamos el vertices por todas las matrices en el orden correcto
    vt = viewportMatrix * projectionMatrix * viewMatrix * modelMatrix @ vt
    
    vt = vt.tolist()[0]
    
    # Dividimos x,y,z por w para regresar el vertices a un tamaño de 3
    vt = [vt[0] / vt[3],
          vt[1] / vt[3],
          vt[2] / vt[3]]
    
    return vt


def fragmentShader(**kwargs):
    # Se lleva a cabo por cada pixel individual
    
    # Obtenemos la informacion requerida
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    
    
    # Empezamos siempre con color blanco
    r = 1
    g = 1
    b = 1
    
    # Para el proposito de mostrar las coordenadas de textura
    # en accion, las usamos para el color
    r *= u
    g *= v
    b *= w
        
    # Se regresa el color
    return [r,g,b]
