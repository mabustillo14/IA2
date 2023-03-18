from A_estrella import astar, MostrarMapa, DeterminarCoordenadas
import Laberinto as Lab
import itertools
from PIL import Image
import random as rd
import math
import matplotlib.pyplot as plt
import numpy as np

def solucion(A,B,coor_Extremos):
    #coor_Extremos = [Ix, Iy, Fx, Fy]

    if(A == "Inicio"): # Asignar coordenadas del picking
        Ax, Ay = coor_Extremos[0], coor_Extremos[1]   
    else: # Determinar coordenadas de cualquier estante existente
        Ax, Ay = DeterminarCoordenadas(A) # Ya estan casteadas los estantes, no hace falta rehacerlo
   
    if(B =="Fin"): # Asignar coordenadas del picking
        Bx, By = coor_Extremos[2], coor_Extremos[3]
    else: # Determinar coordenadas de cualquier estante existente
        Bx, By = DeterminarCoordenadas(B) # Ya estan casteadas los estantes, no hace falta rehacerlo

    # Obtener el Mapa
    maze = Lab.Mapa()
    
    # Establecer los puntos de comienzo y fin
    # El programa lee las coordenadas como (x,y)
    PuntoStart = (Ax, Ay) # 0,0
    PuntoEnd = (Bx, By) #7,7
    
    #print('\nLa trayectoria solución que se debe seguir es:')
    # Pasamos los parametros del mapa, el punto A y B y devuelve el string solucion
    path = astar(maze, PuntoStart, PuntoEnd) 
    return path



def Graficar(optima_ruta):
    
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

    maze    

    # Mostrar el Mapa con la solucion
    MostrarMapa('./Mapa_solucion/mapa_temple.png','Mapa Temple', maze)

    # Output para interfaz gráfica
    imagen_output = Image.open('./Mapa_solucion/mapa_temple.png')

    return imagen_output




def Secuencia(ordenes, coor_Extremos): # Hacer las rutas hacia cada estante de la permutacion i
    # Generar el trayecto desde el Picking hasta el primer estante
    salida = [solucion("Inicio", ordenes[0], coor_Extremos)]

    # Generar los trayectos entre el resto de los estantes siguiendo el orden de la permutacion
    for i in range(len(ordenes)-1):
        path_it = []
        path_it = solucion(ordenes[i], ordenes[i+1], coor_Extremos)
        path_it.pop(0) # Eliminamos el primer elemento porque se repite con el ultimo del path previo
        salida.append(path_it) 
    
    # Tramo de vuelta al Packing
    path_it = solucion(ordenes[len(ordenes)-1], "Fin", coor_Extremos)
    path_it.pop(0)
    salida.append(path_it)

    return salida



def Temple(ordenes, coor_Extremos):
    print("\n-----------------------")
    print("Calculando Coordenadas...")
    # Separamos por un espacio
    ordenes = ordenes.split(",")
    
    # Extraemos los parametros del laberinto
    cant_Filas, cant_columnas,espaciado_alto, alto, espaciado_ancho, ancho = Lab.ExtraccionDatos()

    # Calculamos cuantos estantes existen
    cant_estantes = alto*ancho*cant_columnas*cant_Filas

    # Convertimos a int cada cadena de texto
    for i in range(len(ordenes)):
        ordenes[i] = int(ordenes[i])
        if(ordenes[i]<0 or ordenes[i]>cant_estantes): # Verificamos que exista ese estante
            return "Error - No se ha encontrado la ruta para uno de los estantes", "Error - Verifique que exista todos los estantes", None, None
    
    # Hacemos una lista con las permutaciones
    permutaciones = list(itertools.permutations(ordenes))
    #print(permutaciones)
    
    print("Comenzo el Temple...")

    # Valores Iniciales y de referencia
    # Valores relativos en cada iteracion del for
    it = rd.randint(0,len(permutaciones)-1) # Escogemos una permutacion aleatoria
    permutacion_it = permutacion_it_rel = list(permutaciones[it])
    optima_ruta = optima_ruta_rel = Secuencia(permutacion_it,coor_Extremos)
    optima_permutacion = optima_permutacion_rel = permutacion_it
    costo_optimo = costo_optimo_rel = sum(len(v) for v in optima_ruta)
 
    # Parametros de las funciones de Temple
    t0=100
    alfa=0.88
    lim_repeticiones = 2*(len(ordenes))
    L = 5
    tf=0.01*t0

    if(len(ordenes))<L: # En caso de que la cantidad de estantes sea menor a la cantidad de iteraciones aleatorias
        L = len(ordenes)-1
    
    # Variables auxiliares
    t=t0
    flag = True
    cont = 0 # Cuenta cuantas veces se ha hecho el temple
    cant_repeticiones = 0

    # Genero una lista con los indices de las posibles combinaciones
    index_permutaciones = []
    for i in range(len(permutaciones)):
        index_permutaciones.append(i)
    

    # Obtenemos la ruta con cada una de las permutaciones
    while(flag==True):
        cont+=1
        
        # Condiciones de Detención: Enfriamiento, Sin Combinaciones o Limite Repeticiones
        if (t<tf or len(index_permutaciones)-1<=2*L or cant_repeticiones>lim_repeticiones):
            flag = False


        # Elegimos el indice de una permutacion al azar 
        i=rd.randint(0,len(index_permutaciones)-1-L)

        for j in range(L):# Analizamos los vecinos superiores cercanos
            #Cada elemento es una tupla, asi que las convertimos a lista
            permutacion_it = list(permutaciones[index_permutaciones[i]]) # Consideramos la permutacion i
            ruta_it = Secuencia(permutacion_it, coor_Extremos) # Calculamos la ruta para esa permutacion
            costo_it = sum(len(v) for v in ruta_it) # Determinamos el coste

            # Eliminamos el indice de esa permutacion para no repetir esta permutacion
            index_permutaciones.pop(i)

            # Funciones del Temple
            delta = costo_it - costo_optimo_rel
            valor_random = rd.random()
            exponencial = math.exp(-(delta/t))
            
            # Probabilidad de encontrar la solucion
            if (valor_random<exponencial or delta<0):
                optima_ruta_rel =  ruta_it
                optima_permutacion_rel = permutacion_it
                costo_optimo_rel = costo_it

        #Actualizar Parametros
        t = alfa * t
        cant_repeticiones +=1

        # Si se obtuvo un mejor resultado, se almacena y se reinicia la cantidad de repiticiones
        if (costo_optimo_rel < costo_optimo):
            optima_ruta =  optima_ruta_rel
            optima_permutacion = optima_permutacion_rel
            costo_optimo = costo_optimo_rel
            cant_repeticiones = 0
        
        #Mostrar resultado de cada iteracion    
        text = "Iteración: " + str(cont) + " - Costo óptimo:" + str(costo_optimo) + " - Temperatura: " + str(t) + " - Combinaciones " + str(len(index_permutaciones)) + "/" + str(len(permutaciones))
        print(text)


    optima_permutacion = ["Picking"] + optima_permutacion + ["Packing"] 
    return costo_optimo, optima_permutacion, optima_ruta, Graficar(optima_ruta)
    #return costo_optimo, optima_permutacion, optima_ruta
    


if __name__ == '__main__': #Para que se pueda usar sin interfaz grafica
    print("----------------TEMPLE SIMULADO----------------")
    print("Ingrese la secuencia de pedidos separado por una coma")
    pedidos = input("Ordenes: ")
    print("Ingrese coordenadas del Picking, separada por coma")
    picking = input("Coordenas x,y: ")
    #picking = "0,0"
    print("Ingrese coordenadas del Packing, separada por coma")
    packing = input("Coordenas x,y: ")
    #packing = "0,5"
    coor_Extremos = picking + "," + packing
    coor_Extremos = coor_Extremos.split(",")
    for i in range(len(coor_Extremos)): # Casteamos de str a int
        coor_Extremos[i] = int(coor_Extremos[i])


    
    #texto = "6, 38, 12, 67, 52, 43, 69, 61" # 75 - 52,6, 12, 69,67, 43, 61, 38
    #texto ="61,69,6,43,38,12"   # 53 - 69,38,61,6,12,43    
    #texto = "33,7,12,23" # 49
    
    
    

    costo_optimo, optima_permutacion, optima_ruta, salida = Temple(pedidos, coor_Extremos)
    


    # Resultados
    print("\n-----------------------")
    print("RESULTADOS:")
    print("\nCosto total del picking óptimo: ", costo_optimo)
    print("Ruta de picking óptima:", optima_permutacion)
    print("Secuencia de pasos óptima")
    print(optima_ruta)

