import matplotlib.pyplot as plt
import Laberinto as Lab
from PIL import Image
import math

class nodoo(): #A cada punto del mapa le calcula los valores de g, h y f
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0 # G es la distancia entre el nodo actual y el nodo inicial
        self.h = 0 # H es la heurística: distancia estimada desde el nodo actual hasta el nodo final
        self.f = 0 # F es el costo total del nodo.
    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    #Definimos los nodos inicial y final
    start_node = nodoo(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = nodoo(None, end)
    end_node.g = end_node.h = end_node.f = 0

    #Creamos la lista abierta y cerrada para nodos
    lista_abierta = [] 
    lista_cerrada = []

    #Agregue el cuadrado inicial (o nodo) a la lista abierta.
    lista_abierta.append(start_node)
    
    cont_it = 0
    max_iterations = (len(maze) // 2)  ** 100

    # Loop hasta encontrar el nodo final
    while len(lista_abierta) > 0:
        

        cont_it += 1
        # si llegamos a este punto, devolvemos el camino, ya que puede que no haya solución o
        # el costo de computación es demasiado alto
        if cont_it > max_iterations:
            print ("Demasiadas iteraciones")
            path = []
            current = nodo_Actual
            while current is not None:
                path.append(current.position)

                #Si en ese path ya aparecio el punto objetivo, que no envie los otros elementos
                if(current.position == end_node.position):    
                    return path[::0]

                # Actualizo el actual por el padre del mismo
                current = current.parent
            path = [start, "Sin Solucion", end]
            return path


        #Busque el cuadrado de costo F más bajo en la lista abierta. Nos referimos a esto como el cuadrado actual
        nodo_Actual = lista_abierta[0]
        current_index = 0
        for index, item in enumerate(lista_abierta):
            if item.f < nodo_Actual.f: # Buscar la celda de menor F
                nodo_Actual = item
                current_index = index
        
        

        # ELiminar la celda actual de la lista abierta, agregar a la lista cerrada
        lista_abierta.pop(current_index)
        lista_cerrada.append(nodo_Actual)
        
        # Condicional de llegar al objetivo
        if nodo_Actual == end_node:
            path = []
            current = nodo_Actual
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] 
        
        # Generar hijos para la siguiente lista abierta
        children = [] # Generamos maximo 4 hijos
        for new_position in [(-1, 0), (1, 0), (0, -1), (0, 1)]: #Solo me puedo mover vertical y horizontalmente
            # Prioridades: Arriba, Abajo, Izquierda, Derecha
            # Obtener la posicion del nodo
            posicion_nodo = (nodo_Actual.position[0] + new_position[0], nodo_Actual.position[1] + new_position[1])
            
            # Si es verdadero se corta esa iteracion
            # Asegurarme que el nodo este dentro de las dimensiones del mapa
            if posicion_nodo[0] > (len(maze) - 1) or posicion_nodo[0] < 0 or posicion_nodo[1] > (len(maze[len(maze)-1]) -1) or posicion_nodo[1] < 0:
                continue
            # Asegurarme que estoy en una casilla sin obstaculo
            if maze[posicion_nodo[0]][posicion_nodo[1]] != 0 and posicion_nodo!=end_node.position:
                continue
             
            # Crear un nuevo nodo- un hijo
            nuevo_node = nodoo(nodo_Actual, posicion_nodo)
            
            # Si pasa todas las pruebas, agregar el nuevo nodo
            children.append(nuevo_node)
        

        # Para cada elemento de la lista children se verifica si ya se analizo antes
        for nodo_children in children:

             # Child is on the closed list
            for nodo_lista_cerrada in lista_cerrada:
                if nodo_children == nodo_lista_cerrada: # Si ya pertenece a la lista cerrada, no se continua analizando lo de abajo
                    continue
                
            #En caso de que no perteneza a la lista cerrada, sucede lo siguiente

            # Calcular f,g,h
            nodo_children.g = nodo_Actual.g + 1 #distancia entre el nodo actual y el nodo inicial
            nodo_children.h = (abs(nodo_children.position[0] - end_node.position[0])) + (abs(nodo_children.position[1] - end_node.position[1])) #Distancia Manhattan
            nodo_children.f = nodo_children.g + nodo_children.h #Costo Total

            # Verificar que no vuelve a una casilla donde ya estuvo
            for nodo_lista_abierta in lista_abierta:

                
                if nodo_children == nodo_lista_abierta and nodo_children.g > nodo_lista_abierta.g: 
                    continue
            
            # Añadir el nodo_children a la lista abierta si paso todas las pruebas
            lista_abierta.append(nodo_children)
    


def MostrarMapa(NombreMapa, titulo, maze):
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
    plt.savefig(NombreMapa)   



def solucion(A,B):
    ESolucion = True

    # Cast: Conversión string a int
    A, B = int(A), int(B)

    Ax, Ay = DeterminarCoordenadas(A)
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
    

    print('\nLa trayectoria solución que se debe seguir es:')
    # Pasamos los parametros del mapa, el punto A y B y devuelve el string solucion
    path = astar(maze, PuntoStart, PuntoEnd) 
    if(path[1]!="Sin Solucion"):
        print(path)
    else:
        ESolucion = False
        path.pop(1)

    # Agregar al Mapa la secuencia de la solucion
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
        maze[lista[i]][lista[i+1]] = 5 
    # Puntos A y B de distinto Color
    maze[lista[0]][lista[1]] = 7 
    maze[lista[len(lista)-2]][lista[len(lista)-1]] = 7 
    # Mostrar el Mapa con la solucion
    MostrarMapa('mapa_solucion.png','Mapa Solución', maze)

    # Output para interfaz gráfica
    imagen_output = Image.open('mapa_solucion.png')

    if ESolucion ==  False:
        path = ["No hay solucion"]
        print(path)

    return path, imagen_output
    



def DeterminarCoordenadas(Mesa):
    cant_Filas, cant_columnas,espaciado_alto, alto, espaciado_ancho, ancho = Lab.ExtraccionDatos()

    cant_estantes = cant_Filas*cant_columnas*alto*ancho
    if(Mesa>cant_estantes):
        return None, None
    
    if(Mesa ==0):
        return 0, 0

    # Determinar el Area de Cada conjunto de estantes
    area_agrupacion = alto*ancho

    # Determinar en que grupo esta
    grupo = math.ceil(Mesa/area_agrupacion)
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
            grupos[i][j] = cont
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
            grupo_relativo[i][j] = cont

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


if __name__ == '__main__': #Para que se pueda usar sin interfaz grafica
    cant_Filas, cant_columnas,espaciado_alto, alto, espaciado_ancho, ancho = Lab.ExtraccionDatos()
    
    print('--------------------Método A*--------------------')
    print("Ingrese el estante correspondiente a cada tramo del recorrido")

    # Determinar en que agrupacion esta la posicion inicial
    aux = alto*ancho*cant_columnas*cant_Filas
    fin = True # Determinar si existe un estante
    while(fin):
        A = int(input ('Estante Inicial: '))

        if(0<=A<=aux):
            fin = False
        else:
            print("Error - Ingrese un estante válido")

    fin = True # Determinar si existe un estante
    while(fin):
        B = int(input ('Estante Objetivo: '))
        if(0<=B<=aux):
            fin = False
        else:
            print("Error - Ingrese un estante válido")



    solucion (A, B)
