from Laberinto_dinamico import DeterminarCoordenadas_AlgGenetico
from A_estrella import astar, MostrarMapa, DeterminarCoordenadas
import Laberinto as Lab
import itertools
from PIL import Image

def solucion(A,B,ordenamiento):
    # Cast: Conversión string a int
    A, B = int(A), int(B)

    if(A ==0):
        Ax, Ay = 0, 0
    else:
        Ax, Ay = DeterminarCoordenadas_AlgGenetico(A,ordenamiento)
   
    if(B ==0):
        Bx, By = 0, 0
    else:
        Bx, By = DeterminarCoordenadas_AlgGenetico(B,ordenamiento)
    
    # Verificar que el estante exista
    if(Ax==None):
        return "Ingrese un estante A válido", None
    elif(Bx==None):
        return "Ingrese un estante B válido", None

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


def Secuencia(ordenes, ordenamiento):
    # Generar el trayecto completo dado una seria de ubicaciones
    salida = [[DeterminarCoordenadas(ordenes[0])]]
    for i in range(len(ordenes)-1):
        path_it = []
        #print(DeterminarCoordenadas(ordenes[i]))
        #print(ordenes[i], ordenes[i+1])
        path_it = solucion(ordenes[i], ordenes[i+1], ordenamiento)
        path_it.pop(0)
        salida.append(path_it) 
    
    #print(salida)
    #costo = sum(len(v) for v in salida)
    #print(costo)
    
    return salida


def Temple(ordenes, ordenamiento):

    # Separamos por un espacio
    ordenes = ordenes.split(",")
    
    cant_Filas, cant_columnas,espaciado_alto, alto, espaciado_ancho, ancho = Lab.ExtraccionDatos()

    # Obtener caracteristicas del Laberinto
    cant_estantes = alto*ancho*cant_columnas*cant_Filas

    # Convertimos a int cada cadena de texto
    for i in range(len(ordenes)):
        ordenes[i] = int(ordenes[i])
        if(ordenes[i]<0 or ordenes[i]>cant_estantes): # Verificamos que exista ese estante
            return "Error - No se ha encontrado la ruta para uno de los estantes", "Error - Verifique que exista todos los estantes", None, None
    
    # Hacemos una lista con las permutaciones
    permutaciones = list(itertools.permutations(ordenes))
    #print(permutaciones)

    permutacion_it = list(permutaciones[0])
    optima_ruta = Secuencia(permutacion_it, ordenamiento)
    optima_permutacion= permutacion_it
    costo_optimo = sum(len(v) for v in optima_ruta)

    # Obtenemos la ruta con cada una de las permutaciones
    for i in range(len(permutaciones)):
        #Cada elemento es una tupla, asi que las convertimos a lista
        permutacion_it = list(permutaciones[i])
        ruta_it = Secuencia(permutacion_it, ordenamiento)

        costo_it = sum(len(v) for v in ruta_it)

        if(costo_it < costo_optimo):
            optima_ruta =  ruta_it
            optima_permutacion = permutacion_it
            costo_optimo = costo_it

        print("Calculando ruta optima " + str(i+1) + " de " + str(len(permutaciones)) + " con costo " + str(costo_it))

    return costo_optimo, optima_permutacion, optima_ruta
    


if __name__ == '__main__': #Para que se pueda usar sin interfaz grafica
    #ordenamiento = [2,1,3,4,5,6,7,8,9,10,11,12]
    ordenamiento = []
    Mesa = "5,9,11,2"
    costo_it, permutacion_it, ruta_it = Temple(Mesa, ordenamiento)
    print(costo_it, permutacion_it, ruta_it)
