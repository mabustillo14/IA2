from Laberinto import def_Mapa
from funciones import ordenar, buscarProducto, Graficar

class Nodo():
    def __init__(self, _fila, _columna, _nombre):
        self.columna = _columna
        self.fila = _fila
        self.nombre = _nombre
        self.inicio = False
        self.meta = False
        self.pasillo = False
        self.estante = False
        self.padre = None
        self.g = 1
        self.h = 9999999
        self.f = 9999999

    def crearPasillo(self):
        self.pasillo = True

    def crearEstante(self):
        self.estante = True

    def crearInicio(self):
        self.inicio = True

    def crearMeta(self):
        self.meta = True

    def esPasillo(self):
        return self.pasillo

    def esEstante(self):
        return self.estante

    def esInicio(self):
        return self.inicio

    def esMeta(self):
        return self.meta

    def heu(self, filaO, columnaO):
        self.h = abs(self.fila-filaO)+abs(self.columna-columnaO)
        self.f = self.h+self.g

    def gcost(self, fila_inicial, columna_inicial):
        self.g = abs(fila_inicial-self.fila)+abs(columna_inicial-self.columna)


def crearNodos(Mapa, _Inicio, _Meta):
    numero = 0

    # Crear Cuadricula de Nodos
    Nodos = []
    for i in range(len(Mapa)): # Filas
      aux = []
      for j in range(len(Mapa[i])):
        aux.append(numero)
      Nodos.append(aux)

    for fila in range(len(Mapa)):
        for columna, valor in enumerate(Mapa[fila]):
            if valor == " P":
                nodo = Nodo(fila, columna, "P"+str(numero))
                numero += 1
                nodo.crearPasillo()
                nodo.heu(_Meta[0], _Meta[1])
                Nodos[fila][columna] = nodo
            elif valor == " I":
                nodo = Nodo(fila, columna, valor)
                nodo.crearInicio()
                nodo.heu(_Meta[0], _Meta[1])
                Nodos[fila][columna] = nodo
            elif valor == " M":
                nodo = Nodo(fila, columna, valor)
                nodo.crearMeta()
                nodo.heu(_Meta[0], _Meta[1])
                Nodos[fila][columna] = nodo
            else:
                nodo = Nodo(fila, columna, valor)
                nodo.crearEstante()
                nodo.heu(_Meta[0], _Meta[1])
                Nodos[fila][columna] = nodo

    Nodos[_Inicio[0]][_Inicio[1]].crearInicio()
    Nodos[_Inicio[0]][_Inicio[1]].heu(_Meta[0], _Meta[1])
    Nodos[_Meta[0]][_Meta[1]].crearMeta()
    Nodos[_Meta[0]][_Meta[1]].heu(_Meta[0], _Meta[1])
    return Nodos


def Algoritmo(Mapa, Inicio, Meta, MostrarData=False): #algoritmo A estrella
    posiX = Inicio[0]
    posiY = Inicio[1]
    posmX = Meta[0]
    posmY = Meta[1]

    Nodos = crearNodos(Mapa, Inicio, Meta)

    cantFilas, cantColumnas = len(Mapa), len(Mapa[0])

    Abiertos = []  # Sucesores sin explorar, ordenados en forma creciente de f
    Cerrados = []  # Nodos ya explorados

    for filas in Nodos:
        for nodo in filas:
            if nodo.esInicio():
                Abiertos.append(nodo)
                # da 0, costo desde el actual al nodo raíz
                nodo.gcost(posiY, posiX)
                nodo.heu(posmY, posmX)  # costo desde el actual a la meta

    # Para agregar los sucesores iniciales
    bordesup = False
    bordeinf = False
    bordeizq = False
    bordeder = False

    if Abiertos[0].fila == 0:
        bordesup = True
    if Abiertos[0].fila == (cantFilas-1):
        bordeinf = True
    if Abiertos[0].columna == 0:
        bordeizq = True
    if Abiertos[0].columna == (cantColumnas-1):
        bordeder = True
     # nodo de abajo
    if Abiertos[0].fila < (cantFilas-1) and Nodos[Abiertos[0].fila + 1][Abiertos[0].columna].esPasillo() and not bordeinf:
        Nodos[Abiertos[0].fila + 1][Abiertos[0].columna].gcost(posiY, posiX)
        Nodos[Abiertos[0].fila + 1][Abiertos[0].columna].heu(posmY, posmX)
        Nodos[Abiertos[0].fila + 1][Abiertos[0].columna].padre = Abiertos[0]
        Abiertos.append(Nodos[Abiertos[0].fila + 1][Abiertos[0].columna])
    # nodo de arriba
    if Abiertos[0].fila > 0 and Nodos[Abiertos[0].fila - 1][Abiertos[0].columna].esPasillo() and not bordesup:
        Nodos[Abiertos[0].fila - 1][Abiertos[0].columna].gcost(posiY, posiX)
        Nodos[Abiertos[0].fila - 1][Abiertos[0].columna].heu(posmY, posmX)
        Nodos[Abiertos[0].fila - 1][Abiertos[0].columna].padre = Abiertos[0]
        Abiertos.append(Nodos[Abiertos[0].fila - 1][Abiertos[0].columna])
    # nodo a la derecha
    if Abiertos[0].columna < (cantColumnas-1) and Nodos[Abiertos[0].fila][Abiertos[0].columna + 1].esPasillo() and not bordeder:
        Nodos[Abiertos[0].fila][Abiertos[0].columna+1].gcost(posiY, posiX)
        Nodos[Abiertos[0].fila][Abiertos[0].columna+1].heu(posmY, posmX)
        Nodos[Abiertos[0].fila][Abiertos[0].columna+1].padre = Abiertos[0]
        Abiertos.append(Nodos[Abiertos[0].fila][Abiertos[0].columna+1])
     # nodo de la izquierda
    if Abiertos[0].columna > 0 and Nodos[Abiertos[0].fila][Abiertos[0].columna - 1].esPasillo() and not bordeizq:
        Nodos[Abiertos[0].fila][Abiertos[0].columna-1].gcost(posiY, posiX)
        Nodos[Abiertos[0].fila][Abiertos[0].columna-1].heu(posmY, posmX)
        Nodos[Abiertos[0].fila][Abiertos[0].columna-1].padre = Abiertos[0]
        Abiertos.append(Nodos[Abiertos[0].fila][Abiertos[0].columna - 1])
 
    Cerrados.append(Abiertos[0])  # AÑADE EL INICIAL A CERRADOS (YA EXPLORADO)
    Abiertos.remove(Abiertos[0])  # SE ELIMINA EL INICIAL
    Abiertos = ordenar(Abiertos)  # SE ORDENAN LOS VECINOS AGREGADOS
    NodoActual = Abiertos[0]  # MEJOR VECINO
    stop = 0
    costo = 0
    while True:
      #Comprobación de Meta
      bordesup=False
      bordeinf=False
      bordeizq=False
      bordeder=False
    
      if NodoActual.fila==0:
        bordesup=True
      if NodoActual.fila==(cantFilas-1):
        bordeinf=True
      if NodoActual.columna==0:
        bordeizq=True
      if NodoActual.columna==(cantColumnas-1):
        bordeder=True
        
      #Verificacion de meta alcanzada     
      meta=0
      if not bordeinf:
        if Nodos[NodoActual.fila + 1][NodoActual.columna].esMeta():
         meta=1
      if not bordesup:
        if Nodos[NodoActual.fila - 1][NodoActual.columna].esMeta():
          meta=1
      if not bordeder:
        if  Nodos[NodoActual.fila][NodoActual.columna + 1].esMeta():
          meta=1
      if not bordeizq:
        if Nodos[NodoActual.fila][NodoActual.columna - 1].esMeta():
          meta=1
      if meta ==1:
        Camino=[]
        
        while NodoActual is not None:
          Camino.append((NodoActual.fila,NodoActual.columna))
          NodoActual=NodoActual.padre
        Camino=list(reversed(Camino))
        Camino.append((Meta[0],Meta[1]))
        if(MostrarData):
          print("\nMETA ALCANZADA")
          print("CAMINO MÁS CORTO:")
          print(Camino)
        
        costo_=len(Camino)
        break
        
      #nodo de abajo
      if not bordeinf:
        if  Nodos[NodoActual.fila + 1][NodoActual.columna].esPasillo()  and not Nodos[NodoActual.fila + 1][NodoActual.columna] in Cerrados and not Nodos[NodoActual.fila + 1][NodoActual.columna] in Abiertos:
          Nodos[NodoActual.fila + 1][NodoActual.columna].gcost(posiY,posiX)
          Nodos[NodoActual.fila + 1][NodoActual.columna].heu(posmY,posmX)
          Nodos[NodoActual.fila + 1][NodoActual.columna].padre=NodoActual
          Abiertos.append(Nodos[NodoActual.fila + 1][NodoActual.columna])    
      #nodo de arriba
      if not bordesup:
        if  Nodos[NodoActual.fila - 1][NodoActual.columna].esPasillo() and not Nodos[NodoActual.fila - 1][NodoActual.columna] in Cerrados and not Nodos[NodoActual.fila - 1][NodoActual.columna] in Abiertos: 
          Nodos[NodoActual.fila - 1][NodoActual.columna].gcost(posiY,posiX)
          Nodos[NodoActual.fila - 1][NodoActual.columna].heu(posmY,posmX)
          Nodos[NodoActual.fila - 1][NodoActual.columna].padre=NodoActual
          Abiertos.append(Nodos[NodoActual.fila - 1][NodoActual.columna])
      #nodo a la derecha
      if not bordeder:
        if Nodos[NodoActual.fila][NodoActual.columna + 1].esPasillo() and not  Nodos[NodoActual.fila][NodoActual.columna + 1] in Cerrados and not Nodos[NodoActual.fila][NodoActual.columna + 1] in Abiertos:
          Nodos[NodoActual.fila][NodoActual.columna+1].gcost(posiY,posiX)
          Nodos[NodoActual.fila][NodoActual.columna+1].heu(posmY,posmX)
          Nodos[NodoActual.fila][NodoActual.columna+1].padre=NodoActual
          Abiertos.append(Nodos[NodoActual.fila][NodoActual.columna+1])
        #nodo de la izquierda
      if not bordeizq:
        if Nodos[NodoActual.fila][NodoActual.columna - 1].esPasillo() and not Nodos[NodoActual.fila][NodoActual.columna - 1] in Cerrados and not Nodos[NodoActual.fila][NodoActual.columna - 1] in Abiertos: 
          Nodos[NodoActual.fila][NodoActual.columna-1].gcost(posiY,posiX)
          Nodos[NodoActual.fila][NodoActual.columna-1].heu(posmY,posmX)
          Nodos[NodoActual.fila][NodoActual.columna-1].padre=NodoActual
          Abiertos.append(Nodos[NodoActual.fila][NodoActual.columna - 1])
      
      if stop >=10000:  
        print("No se encotró la solución")
        break
      stop+=1
      if(MostrarData):
        print("Iteración número:",stop)

      #UNA VEZ AGREGADOS LOS NODOS VECINOS A ABIERTOS:
      Cerrados.append(NodoActual) #AGREGO EL NODO ACTUAL A LOS CERRADOS
      Abiertos.remove(NodoActual)#ELIMINO EL NODO ACTUAL DE ABIERTOS
      Abiertos=ordenar(Abiertos) #ORDENO POR VALOR DE F
      NodoActual=Abiertos[0]#NODO ACTUAL ES EL DE MENOR F EN ABIERTOS
    #return costo_, Camino
    return costo_, Camino

def calcularCosto(orden, _NodosAux, _Inicio, Mapa):
    costoT = 0
    InicioAux = _Inicio
    for producto in orden:
        costoIt, camino = Algoritmo(Mapa, InicioAux,buscarProducto(_NodosAux, producto))
        costoT += costoIt
        InicioAux = buscarProducto(_NodosAux, producto)
    costoIt, camino = Algoritmo(Mapa, buscarProducto(_NodosAux, producto), _Inicio)
    costoT += costoIt
    return costoT
####################################### GUI #########################################################

def GUI(InicioX, InicioY, MetaX, MetaY):
  Inicio = [int(InicioX), int(InicioY)]
  Meta = [int(MetaX), int(MetaY)]
  
  Mapa = def_Mapa()
  cantFilas, cantColumnas = len(Mapa), len(Mapa[0])

  if(Inicio[0]>cantFilas or         Inicio[1]>cantColumnas):
    return "Error - Coordenada Inicial fuera del Laberinto", None, None

  if(Meta[0]>cantFilas or Meta[1]>cantColumnas):
    return "Error - Coordenada Objetivo fuera del Laberinto", None, None
  
  costo, camino = Algoritmo(Mapa, Inicio, Meta, True)
  img = Graficar(Mapa, [camino], "Temple Lineal Simulado")
  return costo, camino, img


####################################### MAIN #########################################################


if __name__ == '__main__': #Para que se pueda usar sin interfaz grafica
    Mapa = def_Mapa()
     
    cantFilas, cantColumnas = len(Mapa), len(Mapa[0])

    while True:
        print("Ingrese coordenada X del inicio (FILA) (Entrada al almacén): ")
        posiX = int(input())
        print("Ingrese coordenada Y del inicio (COLUMNA)(Entrada al almacén): ")
        posiY = int(input())
        
        if  posiY<=(cantColumnas-1) and posiX <=(cantFilas-1): #(posiY==0 or posiX==0 or posiY == 17 or posiX == 17)
            #if Mapa[posiX][posiY] == " P":
            Mapa[posiX][posiY] = " I"
            Inicio=[posiX,posiY]
            break
            #else:
            #    print ("El inicio no puede estar encima de un producto. Debe estar en los laterales del almacén")
        else:
            print("Coordenada fuera del Mapa")


    while True:
        print("Ingrese coordenada X de la meta (FILA) (Producto a buscar): ")
        posmX = int(input())
        print("Ingrese coordenada Y de la meta (COLUMNA) (Producto a buscar): ")
        posmY = int(input())

        if  posmY<=(cantColumnas-1) and posmX <=(cantFilas-1):
            #if Mapa[posmX][posmY] != " P":
                Mapa[posmX][posmY] = " M"
                Meta=[posmX,posmY]
                break
            #else:
            #    print ("La meta debe ser la posición de un producto.")
        else:
            print("Coordenada fuera del Mapa")



    #AlgoritmoAestrella(Mapa,Meta,posiY,posiX,posmY,posmX)
    #camino, costo = AlgoritmoAestrella(Mapa, Inicio, Meta) #algoritmo A estrella
    costo, camino = Algoritmo(Mapa, Inicio, Meta, True) #algoritmo A estrella
    print("Costo:", costo)
    print("Camino:", camino)

    #Graficar(camino, "Mapa A Estrella", "A Estrella")    
    img = Graficar(Mapa, [camino], "Temple Lineal Simulado")
