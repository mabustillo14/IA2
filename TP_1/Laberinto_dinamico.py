import math


cant_filas = 2
cant_columnas = 2
ancho=2
largo=3
espaciado_alto = 2
espaciado_ancho = 2



def DeterminarCoordenadas_AlgGenetico(Mesa, ordenamiento):
#    cant_Filas, cant_columnas,espaciado_alto, alto, espaciado_ancho, ancho = Lab.ExtraccionDatos()

    cant_Filas = 1
    cant_columnas = 2
    espaciado_alto = 1 
    alto = 3 
    espaciado_ancho = 1
    ancho = 2

    cant_estantes = cant_Filas*cant_columnas*alto*ancho
    if(Mesa>cant_estantes):
        return None, None
    
    if(Mesa ==0):
        return 0, 0

    # Determinar el Area de Cada conjunto de estantes
    area_agrupacion = alto*ancho

    # Determinar en que grupo esta
    for i in range(len(ordenamiento)):
        #print(ordenamiento[i])
        if(Mesa == ordenamiento[i]):
            grupo = math.ceil(i/area_agrupacion) 
    #print(grupo)
 

    # Generemos una matriz con la distribucion de los grupos
    grupos = [] # Matriz de la distribucion de los grupos
    
    # Creamos la matriz llena de ceros
    for i in range(cant_Filas):
        filas =  []
        for j in range(cant_columnas):
                filas.append(0)
        grupos.append(filas)
    #print(grupos)

    
    cont = 0
    # Determinar el desplazamiento de cada conjunto respecto al origen (se toma la esquina superior izquierda como 0)
    x_grupo=0
    y_grupo=0
    for i in range(cant_columnas): # La numeración se completa primero en filas y despues las columnas
        for j in range(cant_Filas):
            cont +=1
            grupos[j][i] = cont
    
            if (cont == grupo) :
                x_grupo = j
                y_grupo = i

    
    #print("Desp grupo", x_grupo, y_grupo)
    x_inicial = espaciado_alto
    y_inicial = espaciado_ancho
    
    # Desplazamiento para llegar al primer cuadrado del conjunto desde el 0,0
    x_absoluto = x_inicial + x_grupo*(alto + espaciado_alto)   
    y_absoluto = y_inicial + y_grupo*(ancho + espaciado_ancho)

    #print("Absolutos ",x_absoluto, y_absoluto)
    
    # Determinar el desplazamiento relativo dentro de cada grupo
    grupo_relativo = []
    cont = 0
    
    # Generamos la matriz relativa    
    for i in range(alto):
        filas =  []
        for j in range(ancho):
                filas.append(0)
        grupo_relativo.append(filas)
    
    # Determinar el conjunto de valores dentro este grupo, referidos a un rango de 0 a area_agrupacion
    aux = Mesa-(grupo-1)*area_agrupacion

    # Determinamos el desplazamiento relativo desde el 0,0 del grupo
    for i in range(alto):
        for j in range(ancho):
            cont +=1
            grupo_relativo[i][j] = ordenamiento[cont]

            if (cont == aux):
                x_rel = i
                y_rel = j
    
    #for i in range(len(grupo_relativo)):
    #    print(grupo_relativo[i])
    #print("rel", x_rel, y_rel)

    # Calcular la posicion de desplazamiento desde el origen 0,0
    x_final = x_absoluto + x_rel
    y_final = y_absoluto + y_rel

    #print("final", x_final,y_final)
    
    return x_final,y_final





"""
# Asignar valores
cant_estantes = cant_filas*ancho*cant_columnas*largo

# Crear lista con las etiquetas
estantes = []
for i in range(1,cant_estantes):
    estantes.append(i)
"""

#ordenamiento = [1,2,3,4,5,6,7,8,9,10,11,12]
#Mesa = 5
#x, y = DeterminarCoordenadas_AlgGenetico(Mesa, ordenamiento)