import Laberinto as Lab
#from Algoritmo_genetico import Alg_Genetico
from PIL import Image
import matplotlib.pyplot as plt
import itertools


from A_estrella import astar


from PIL import Image
import random as rd
import math
import matplotlib.pyplot as plt
import numpy as np

###---------------------------- METODOS DE A ESTRELLA ----------------------------
def solucionAstar(A,B): # Distancia entre 2 estantes o puntos
    # Debo pasar las coordenadas de cada estante como una lista
    # [1,2] coordenada -- [1,None] numero de estante
    cant_Filas, cant_columnas,espaciado_alto, alto, espaciado_ancho, ancho = Lab.ExtraccionDatos()
    cant_estantes = cant_Filas*cant_columnas*alto*ancho
    
    
    # Establecer la enumeracion de las mesas
    Enumeracion = []
    for i in range(1,cant_estantes):
        Enumeracion.append(i)
    
    # Obtener coordenadas de cada mesa

    if(A[1]==None):
        Ax, Ay = DeterminarPosicion(A[0], Enumeracion)
    else:
        Ax, Ay = A[0], A[1]


    if(B[1]==None):
        Bx, By = DeterminarPosicion(B[0], Enumeracion)
    else:
        Bx, By = B[0], B[1]

    # Verificar que el estante exista
    if(Ax==None or Bx==None):
        print("---Ingrese un estante válido---")
        return "Error"
    
    # Obtener el Mapa
    maze = Lab.Mapa()
    
    # Establecer los puntos de comienzo y fin
    # El programa lee las coordenadas como (x,y)
    PuntoStart = (Ax, Ay) # 0,0
    PuntoEnd = (Bx, By) #7,7
    
    path = astar(maze, PuntoStart, PuntoEnd)
    return path


def solucionAstar_optimizado(A,B): # Buscar distancia entre 2 estantes en la matriz precalculada
    # INPUT: Numero del estante
    mapa_distancias=Extraer_Distancias()
    
    # Ubicar distancia en la matriz
    A -= 1 # Por la fila 0 y columna 0
    B -= 1
    return mapa_distancias[A][B] 






###---------------------------- METODOS DE GUI ----------------------------
def Graficar(optima_ruta, NombreArchivo, titulo):
    # optima_ruta es una lista de listas    
    # Obtener el Mapa
    maze = Lab.Mapa()
    cont = 4 # El 0 y 1 representan obstaculos y espacios libres, el 2 los puntos de recolección
    for j in range(len(optima_ruta)):
        path = optima_ruta[j]
        lista = []
        
        # Graficar cada lista 
        for i in range(len(path)): # El sistema de referencia esta invertido
            num1 = path[i][0] # Coordenada Y
            num2 = path[i][1] # Coordenada X

            # Pasamos las coordenadas a graficar como (y,x)
            # Los ejes estan invertidos
            lista.append(num1)
            lista.append(num2)
        

        # Colorear los puntos del path
        for i in range(0,len(lista),2):
            maze[lista[i]][lista[i+1]] = cont
        cont +=1

    # Mostrar el Mapa con la solucion
    path_img = MostrarMapa(NombreArchivo,titulo, maze)

    # Output para interfaz gráfica
    imagen_output = Image.open(path_img)
    return imagen_output

def MostrarMapa(NombreArchivo, titulo, maze):
    # Generar Figura
    plt.matshow(maze)
    # Agregar nombre a los ejes
    # Los ejes estan invertidos
    plt.xlabel("Coordenada Y", size = 16,)
    plt.ylabel("Coordenada X", size = 16)
    
    # Agregar el titulo
    plt.title(
        titulo, 
        fontdict={'color':'black', 'size':16},
        loc='center')
    #plt.grid(color='b', linestyle='-', linewidth=0.5)
    # Guardar figura
    path_img = './Mapa_solucion/'+ NombreArchivo +'.png'
    
    plt.savefig(path_img) 

    return path_img  






###---------------------------- METODOS DE POSICION Y DISTANCIA ----------------------------
def DeterminarPosicion(Mesa, Enumeracion): 
    # Enumeracion se refiere a como estan enumerados cada estante

    cant_Filas, cant_columnas,espaciado_alto, alto, espaciado_ancho, ancho = Lab.ExtraccionDatos()

    cant_estantes = cant_Filas*cant_columnas*alto*ancho
    if(Mesa>cant_estantes):
        return None, None
    
    if(Mesa ==0):
        return 2, 2

    # Determinar el Area de Cada conjunto de estantes
    area_agrupacion = alto*ancho

    # Determinar en que grupo esta
    #grupo = math.ceil(Mesa/area_agrupacion)

    for i in range(len(Enumeracion)):
        if (Mesa == Enumeracion[i]):
            grupo = math.ceil(i/area_agrupacion)
    #print(grupo)

    # Generemos una matriz con la distribucion de los grupos
    grupos = []
    cont = 0
    # Creamos la matriz llena de ceros
    for i in range(cant_Filas):
        filas =  []
        for j in range(cant_columnas):
                filas.append(0)
        grupos.append(filas)
    #print(grupos)
    # Determinar el desplazamiento de cada conjunto respecto al origen (se toma la esquina superior izquierda como 0)
    x_grupo=0
    y_grupo=0
    for i in range(cant_columnas): # La numeración se completa primero en filas y despues las columnas
        for j in range(cant_Filas):
            cont +=1
            #grupos[i][j] = cont
            #grupos[j][i] = cont
            if (cont == grupo) : # Determinar coordenadas del conjunto de tableros
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
    
    
    # Generamos la matriz relativa, llena de ceros    
    for i in range(alto):
        filas =  []
        for j in range(ancho):
                filas.append(0)
        grupo_relativo.append(filas)

    # Determinar el conjunto de valores dentro este grupo, referidos a un rango de 0 a area_agrupacion
    #aux = Mesa-(grupo-1)*area_agrupacion
    cont = alto * ancho * (grupo - 1)  + 1 
    #print(cont)
    # Determinamos el desplazamiento relativo desde el 0,0 del grupo
    x_rel, y_rel = 0,0
    for i in range(alto):
        for j in range(ancho):
            
            #grupo_relativo[i][j] = cont

            if (Enumeracion[cont-1] == Mesa):
                x_rel = i
                y_rel = j
            
            cont +=1

    #for i in range(len(grupo_relativo)):
    #    print(grupo_relativo[i])
    #print("rel", x_rel, y_rel)

    # Calcular la posicion de desplazamiento desde el origen 0,0
    x_final = x_absoluto + x_rel
    y_final = y_absoluto + y_rel

    #print("final", x_final,y_final)
    return x_final,y_final


def Extraer_Distancias():
    Distancias = []

    # Extraer los objetos del txt
    with open("mediciones.txt") as archivo:
        for linea in archivo:
            datos = linea.split(",")
            datos.pop(0) # Eliminamos el estante de inicio
            datos.pop(len(datos)-1) # Elimino el salto de linea
            #print(datos)
            Distancias.append(datos)

    # Castear cada uno de los valores
    for i in range(len(Distancias)): # Estante de Inicio
        for j in range(len(datos)): # Estante objetivo
            Distancias[i][j] = int(Distancias[i][j])
    
    return Distancias






if __name__ == '__main__': #Para que se pueda usar sin interfaz grafica
    print(solucionAstar([1, None], [6, None]))

    # Con el metodo optimizado
    print(solucionAstar_optimizado(1, 6))
