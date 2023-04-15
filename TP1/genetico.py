import random
import math
import cProfile, pstats, io
from pstats import SortKey
import matplotlib.pyplot as plt

from funciones import ordenar, estadosVecinos, buscarProducto
from A_ESTRELLA import crearNodos, Algoritmo, calcularCosto
from Laberinto import def_Mapa
from templeLineal import TempleLineal


def crearMapa(productos): # Creamos un mapa para una iteracion
    # Usamos el armazon del almacen y rehacemos el laberinto
    Map = def_Mapa()
    for i in range(len(Map)):
        for j in range(len(Map[i])):

            if (Map[i][j] != " P"): # Cualquier cuadricula diferente de pasillo
                Map[i][j] = " E" # Le asignamos que es un estante
                    
    i = 0 # indice de estantes encontrados
    for fila in range(len(Map)):
        for columna, valor in enumerate(Map[fila]):
            if valor == " E":
                # elegido=random.choice(productos)
                Map[fila][columna] = str(productos[i])
                # productos.remove(elegido)
                i += 1
    return Map

def Extraccion_Ordenes():
    lineas = []
    with open("ordenes.txt", "r") as archivo:
            for linea in archivo:
                lineas.append(linea) # Agregamos las lineas limpias

    # Limpiamos la lista
    cont = 0
    index_vacios = []
    for linea in lineas:
        linea.strip() # Quitar espacios en blanco
        linea = linea.replace("\n","") #Eliminar el \n de cada linea
        linea = linea.replace("P", "") # Eliminar la P de cada pedido (P20->20)
        lineas[cont] = linea # Actualizamos

        if (linea == ""): # Detectamos saltos de linea/ espacios vacios
            index_vacios.append(cont)
        cont+=1 

    index_vacios.append(len(lineas)) # Agregamos el indice del ultimo elemento

    inicio = 1
    salida = []
    for espacio in index_vacios:
        aux = []
        for i in range(inicio, espacio):
            aux.append(lineas[i])
        inicio = espacio + 2
        salida.append(aux)
    
    return salida

def cruceOrden(individuo1,individuo2):
    corte1=random.randint(1,99)
    corte2=random.randint(1,99)
    while corte2<=corte1:
        corte2=random.randint(1,99)

    ind1aux=[]
    ind2aux=[]
    
    for numeros in range(corte1,corte2):
        ind1aux.append(individuo2[numeros])
        ind2aux.append(individuo1[numeros])

    for prod in individuo1:
        if (prod not in ind1aux) and len(ind1aux)<=len(individuo1)-1-corte1:
            ind1aux.append(prod)
    pos=0
    for prod in individuo1:
        if (prod not in ind1aux) and len(ind1aux)<=len(individuo1)-1:
            ind1aux.insert(pos,prod)
            pos+=1
    
    for prod in individuo2:
        if (prod not in ind2aux) and len(ind2aux)<=len(individuo2)-1-corte1:
            ind2aux.append(prod)
    pos=0
    for prod in individuo2:
        if (prod not in ind2aux) and len(ind2aux)<=len(individuo2)-1:
            ind2aux.insert(pos,prod)
            pos+=1

    return ([ind1aux,ind2aux])

def eleccion_prob(lista): #recibe una lista con los costos de cada individuo de la población

    probabilidad=[]
    for c in range(10):
        lista[c]=1/lista[c]
    suma=float(sum(lista))
    for c in range(10):

        probabilidad.append(((lista[c]/suma)*100))

    prob=random.randint(0, 99)
    if prob>=0 and prob<probabilidad[0]:
        indice=0
    if prob>=probabilidad[0] and prob<probabilidad[0]+probabilidad[1]:
        indice=1
    if prob>=probabilidad[0]+probabilidad[1] and prob<probabilidad[0]+probabilidad[1]+probabilidad[2]:
        indice=2
    if prob>=probabilidad[0]+probabilidad[1]+probabilidad[2] and prob<probabilidad[0]+probabilidad[1]+probabilidad[2]+probabilidad[3]:
        indice=3
    if prob>=probabilidad[0]+probabilidad[1]+probabilidad[2]+probabilidad[3] and prob<probabilidad[0]+probabilidad[1]+probabilidad[2]+probabilidad[3]+probabilidad[4]:
        indice=4
    if prob>=probabilidad[0]+probabilidad[1]+probabilidad[2]+probabilidad[3]+probabilidad[4] and prob<probabilidad[0]+probabilidad[1]+probabilidad[2]+probabilidad[3]+probabilidad[4]+probabilidad[5]:
        indice=5
    if prob>=probabilidad[0]+probabilidad[1]+probabilidad[2]+probabilidad[3]+probabilidad[4]+probabilidad[5] and prob<probabilidad[0]+probabilidad[1]+probabilidad[2]+probabilidad[3]+probabilidad[4]+probabilidad[5]+probabilidad[6]:
        indice=6
    if prob>=probabilidad[0]+probabilidad[1]+probabilidad[2]+probabilidad[3]+probabilidad[4]+probabilidad[5]+probabilidad[6] and prob<probabilidad[0]+probabilidad[1]+probabilidad[2]+probabilidad[3]+probabilidad[4]+probabilidad[5]+probabilidad[6]+probabilidad[7]:
        indice=7
    if prob>=probabilidad[0]+probabilidad[1]+probabilidad[2]+probabilidad[3]+probabilidad[4]+probabilidad[5]+probabilidad[6]+probabilidad[7] and prob<probabilidad[0]+probabilidad[1]+probabilidad[2]+probabilidad[3]+probabilidad[4]+probabilidad[5]+probabilidad[6]+probabilidad[7]+probabilidad[8]:
        indice=8
    if prob>=probabilidad[0]+probabilidad[1]+probabilidad[2]+probabilidad[3]+probabilidad[4]+probabilidad[5]+probabilidad[6]+probabilidad[7]+probabilidad[8] and prob<probabilidad[0]+probabilidad[1]+probabilidad[2]+probabilidad[3]+probabilidad[4]+probabilidad[5]+probabilidad[6]+probabilidad[7]++probabilidad[8]+probabilidad[9]:
        indice=9
    return indice


#########  ALGORITMO GENÉTICO#########
def Genetico():

    pr = cProfile.Profile()
    pr.enable()
    listaOrdenes = Extraccion_Ordenes()
    # crea una lista para almacenar los productos en un orden aleatorio sin repetir.
    matriz=[]
    for i in range(0,10):
        productos=[]
        productosorden=[]
        for numeros in range(0,100):
            productos.append(str(numeros))  #crea una lista con productos del 0 al 99
        for i in range(0,100):
            elegido=random.choice(productos) #elige un elemento de la lista productos al azar
            productosorden.append(elegido) #guardamos ese producto en una lista auxiliar
            productos.remove(elegido) #eliminamos el producto de la lista creada en el bucle for anterior
        matriz.append(productosorden)
    ########### MATRIZ CONTIENE 10 ORDENAMIENTOS AL AZAR (población inicial de 10 individuos) ##########
    print("Generacion 0 creada...")
    generacion=1
    stop = 0

    costoordenes=[]
    while generacion<=3:
        while stop < 10:
            print("#")
            if generacion==1:
                Mapa = crearMapa(matriz[stop])
            elif generacion==2:
                Mapa = crearMapa(matriz[stop+10])
            Costos = []
            for i in range(0, len(listaOrdenes)-1):
                Inicio = [0,0]
                deltaT =  1
                costo_it = TempleLineal(Mapa, Inicio, listaOrdenes[i], deltaT)
                #costo_it = Temple(listaOrdenes[i], Mapa)
                Costos.append(costo_it)
            sumacostos = sum(Costos)
            costoordenes.append(int(sumacostos))  #ACA GUARDAMOS EL COSTO DE CADA ORDENAMIENTO
            stop += 1
            
        print("\n")
        stop=0
        generacion+=1

        
        ### SELECCIONO 2 INDIVIDUOS BAJO CIERTA PROBABILIDAD Y HAGO EL CROSSOVER, REPITO HASTA COMPLETAR DE INDIVIDUOS LA SIGUIENTE GENERACIÓN #### 
        ind=0
        individuos=[]
        print("Proceso de Crossover...")
        if generacion-1<3:
            while ind<5:
                if generacion-1==1:
                    selA=matriz[eleccion_prob(costoordenes)] #eleccion_prob me devuelve el índice de uno de los elementos de la lista matriz, por probabilidad el menor costo 
                    selB=matriz[eleccion_prob(costoordenes)]
                    while selA==selB:
                        selB=matriz[eleccion_prob(costoordenes)]
                elif generacion-1==2:
                    selA=matriz[10+eleccion_prob(costoordenes[10:])]
                    selB=matriz[10+eleccion_prob(costoordenes[10:])]
                    while selA==selB:
                        selB=matriz[10+eleccion_prob(costoordenes[10:])]

                individuos.append(cruceOrden(selA,selB))
                for vect in individuos:
                    for indi in vect:
                        matriz.append(indi)
                ind+=1
                individuos.clear()
                individuos=[]
            print(f"Generacion {generacion-1} creada...")
    print("costoordendes: ",costoordenes)
    costmin=costoordenes[:].index(min(costoordenes[:]))
    print(f"El mejor ordenamiento es {matriz[costmin]} y su costo es {min(costoordenes[:])}")

    ## ESTADÍSTICAS DE TIEMPO
    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

    """
    ## GRAFICO
    i=0
    CostGen=[]
    Generaciones=[0,1,2]
    for iter in range(3):
        mini=costoordenes.index(min(costoordenes[i:i+10]))
        CostGen.append(costoordenes[mini])
        i+=10
    fig, ax = plt.subplots()
    ax.plot(Generaciones, CostGen)
    plt.xlabel("Generacion", size = 16)
    plt.ylabel("Costo del mejor individuo", size = 16)
    ax.set_title("Evolucion de los costos en funcion de la generacion",loc="center")
    plt.xticks([0, 1, 2])
    plt.show()

    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], costoordenes[0:10], color = 'tab:purple', label = 'generacion 0')
    ax.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], costoordenes[10:20], color = 'tab:green', label = 'generacion 1')
    ax.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], costoordenes[20:30], color = 'tab:red', label = 'generacion 2')
    ax.set_xlabel("Individuos")
    ax.set_ylabel("Costos")
    ax.legend(loc = 'upper right')
    plt.show()
    """

if __name__ == '__main__': #Para que se pueda usar sin interfaz grafica
    Genetico()
    #print(Extraccion_Ordenes())