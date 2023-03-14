from A_estrella import astar, MostrarMapa, DeterminarCoordenadas
import Laberinto as Lab
import itertools

def solucion(A,B):
    # Cast: Conversión string a int
    A, B = int(A), int(B)

    if(A ==0):
        Ax, Ay = 0, 0
    else:
        Ax, Ay = DeterminarCoordenadas(A)
   
    if(B ==0):
        Bx, By = 0, 0
    else:
        Bx, By = DeterminarCoordenadas(B)
    
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


def Secuencia(ordenes):
    # Generar el trayecto completo dado una seria de ubicaciones
    salida = [[DeterminarCoordenadas(ordenes[0])]]
    for i in range(len(ordenes)-1):
        path_it = []
        #print(DeterminarCoordenadas(ordenes[i]))
        #print(ordenes[i], ordenes[i+1])
        path_it = solucion(ordenes[i], ordenes[i+1])
        path_it.pop(0)
        salida.append(path_it) 
    
    #print(salida)
    #costo = sum(len(v) for v in salida)
    #print(costo)
    
    return salida

def Graficar(optima_ruta,ordenes):
    # Graficar cada lista 
    # Obtener coordenadas estantes
    coor_ordenes = []
    for i in range(len(ordenes)):
        x, y = DeterminarCoordenadas(ordenes[i])
        coor_ordenes += (x,y)

    # Obtener el Mapa
    maze = Lab.Mapa()
    cont = 4 # El 0 y 1 representan obstaculos y espacios libres, el 2 los puntos de recolección
    for j in range(len(optima_ruta)):

        path = optima_ruta[j]
        lista = []
        
        for i in range(len(path)): # El sistema de referencia esta invertido
            num1 = path[i][0] # Coordenada Y
            num2 = path[i][1] # Coordenada X

            # Pasamos las coordenadas a graficar como (y,x)
            # Los ejes estan invertidos
            lista.append(num1)
            lista.append(num2)

        # Colorear los puntos solucion
        for i in range(0,len(lista),2):
            maze[lista[i]][lista[i+1]] = cont
        cont += 1 #Me ayuda a asignar los colores
        coor_x, coor_y = DeterminarCoordenadas(ordenes[j])
        maze[coor_x][coor_y] = 2 # Estante

    # Graficamos el punto de inicio de otro color
    x, y = optima_ruta[0][0]
    maze[x][y] = 3 # Punto de Inicio

    # Mostrar el Mapa con la solucion
    MostrarMapa('mapa_temple.png','Mapa Temple', maze)




A=5
B=25
C=33
D = 15

ordenes=[A, B, C, D]
# Hacemos una lista con las permutaciones
permutaciones = list(itertools.permutations(ordenes))
#print(permutaciones)

permutacion_it = list(permutaciones[0])
optima_ruta = Secuencia(permutacion_it)
optima_permutacion= permutacion_it
costo_optimo = sum(len(v) for v in optima_ruta)

# Obtenemos la ruta con cada una de las permutaciones
for i in range(len(permutaciones)):
    #Cada elemento es una tupla, asi que las convertimos a lista
    permutacion_it = list(permutaciones[i])
    ruta_it = Secuencia(permutacion_it)

    costo_it = sum(len(v) for v in ruta_it)

    if(costo_it < costo_optimo):
        optima_ruta =  ruta_it
        optima_permutacion = permutacion_it
        costo_optimo = costo_it

    print("Calculando ruta optima " + str(i+1) + " de " + str(len(permutaciones)) + " con costo " + str(costo_it))

# Resultados

print("\nCosto total optimo: ", costo_optimo)
print("Permutacion optima", optima_permutacion)
print("Ruta optima")
print(optima_ruta)
Graficar(optima_ruta,ordenes)
