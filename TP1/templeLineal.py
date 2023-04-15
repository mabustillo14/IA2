import random
import math
import matplotlib.pyplot as plt

from A_ESTRELLA import Algoritmo, crearNodos, calcularCosto
from Laberinto import def_Mapa
from funciones import buscarProducto, estadosVecinos



def TempleLineal(Mapa, Inicio, orden, deltaT, MostrarData=False):
    
    T = 10
    #deltaT = 0.01
    
    NodosAux = crearNodos(Mapa, Inicio, [1, 1]) # LO UTILIZO PARA BUSCAR LA UBICACION DE LOS PRODUCTOS
    cantidadEstados = math.factorial(len(orden)-1)
    espacioBusqueda = cantidadEstados//2
    estadosvisitados = []
    Tgraf=[]
    Cgraf=[]
    

    while T > 0:
        if(MostrarData):
            print("T:", T)
        Tgraf.append(float(T))
        costoActual = calcularCosto(orden, NodosAux, Inicio, Mapa)
        Cgraf.append(int(costoActual))
        while True:
            ordenAux = random.choice(estadosVecinos(orden[:], espacioBusqueda))
            for ordenes in estadosvisitados:
                if ordenAux == ordenes[0]:
                    ordenAux = random.choice(
                        estadosVecinos(orden[:], espacioBusqueda))
            else:
                break
        costoSucesor = calcularCosto(ordenAux, NodosAux, Inicio, Mapa)
        if costoActual >= costoSucesor:
            orden = ordenAux
            estadosvisitados.append([orden[:], costoSucesor])
            costoActual = costoSucesor
            #ESTADO VECINO ACEPTADO POR DELTA
        else:
            prob = random.uniform(0, 1)
            x = -abs(costoActual-costoSucesor)/T
            crit = math.exp(x)
            if prob <= crit:
                orden = ordenAux
                estadosvisitados.append([orden[:], costoSucesor])
                costoActual = costoSucesor
                #ESTADO VECINO ACEPTADO POR PROBABILIDAD
        T -= deltaT
    mejorCosto=9999
    mejorVecino=[0,0]

    if(MostrarData):
        print("\n Datos Calculados")

    for elementos in estadosvisitados:
        
        if(MostrarData):
            print(elementos)
        
        if elementos[1]<=mejorCosto: #elementos 1 es el costo
            mejorCosto=elementos[1]
            mejorVecino=elementos
    #print("ESTADO Y COSTO FINAL", estadosvisitados[len(estadosvisitados)-1])
    
    if(MostrarData):
        print("\nRESULTADOS:")
        print("Mejor Estado:",mejorVecino[0])
        print("Mejor Costo:",mejorVecino[1])
    
    
    """
    fig, ax = plt.subplots()
    ax.plot(Tgraf, Cgraf)
    plt.xlabel("Temperatura (°C)", size = 16)
    plt.ylabel("Costo", size = 16)
    ax.set_title("Evolucion de los costos en funcion del decrecimiento de T lineal",loc="center")
    ax.invert_xaxis()
    plt.show()
    """
    return mejorCosto


########################### MAIN ##################################################################
if __name__ == '__main__': #Para que se pueda usar sin interfaz grafica

    Mapa = def_Mapa()
    Inicio = [0, 0]
    orden = [" 2", " 9", "36", "25", "11"," 4","54","62","88","94","44","40","70","82"]
    MostrarData = True
    deltaT = 0.01
    mejorCosto = TempleLineal(Mapa, Inicio, orden, deltaT, MostrarData)
    