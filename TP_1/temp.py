from funciones import solucionAstar, solucionAstar_optimizado
import Laberinto as Lab
import random as rd
import math


def costo_secuencia(ordenes, coor_Extremos,  enumeracion): # Determinar costo de una ruta
    
    # Costo del picking al primer estante
    ruta_picking = solucionAstar([coor_Extremos[0], coor_Extremos[1]], [ordenes[0], None])
    costo_tot = len(ruta_picking)-1

    # Costo para llegar a cada estante
    for i in range(len(ordenes)-1):
        costo_tot += solucionAstar_optimizado(ordenes[i], ordenes[i+1])
        
    # Tramo de vuelta al Packing
    ruta_packing = solucionAstar([ordenes[len(ordenes)-1], None],[coor_Extremos[2], coor_Extremos[3]])
    costo_tot += len(ruta_packing)-1
    
    return costo_tot


def Temple(ordenes, picking, packing):
    # Extraemos los parametros del laberinto
    cant_Filas, cant_columnas,espaciado_alto, alto, espaciado_ancho, ancho = Lab.ExtraccionDatos()

    # Calculamos cuantos estantes existen
    cant_estantes = alto*ancho*cant_columnas*cant_Filas


    enumeracion = []
    # Asignar valores
    for i in range(1,cant_estantes):
        enumeracion.append(i)

    coor_Extremos = picking + "," + packing
    coor_Extremos = coor_Extremos.split(",")
    for i in range(len(coor_Extremos)): # Casteamos de str a int
        coor_Extremos[i] = int(coor_Extremos[i])

    print("\n-----------------------")
    print("Calculando Coordenadas...")
    # Separamos por un espacio
    ordenes = ordenes.split(",")

    # Convertimos a int cada cadena de texto
    for i in range(len(ordenes)):
        ordenes[i] = int(ordenes[i])
        if(ordenes[i]<0 or ordenes[i]>cant_estantes): # Verificamos que exista ese estante
            return "Error - No se ha encontrado la ruta para uno de los estantes", "Error - Verifique que exista todos los estantes", None
        
    print("Comenzo el Temple...")

    # Valores Iniciales
    permutacion_it_rel = optima_permutacion = permutacion_it = ordenes 
    costo_optimo = costo_optimo_rel = costo_secuencia(permutacion_it,coor_Extremos, enumeracion)

    # Parametros de las funciones de Temple
    t=t0=100
    alfa=0.88

    L = len(ordenes)
    lim_repeticiones = L**2
    tf=0.01*t0

    # Variables auxiliares
    flag = True
    cont = 0 # Cuenta cuantas veces se ha hecho el temple
    cant_repeticiones = 0 # cantidad de veces de obtener la misma respuesta   
    it=0
   

    while(flag==True):
        cont+=1
        
        # Condiciones de Detención: Enfriamiento, Sin Combinaciones o Limite Repeticiones
        if (t<tf or cant_repeticiones>lim_repeticiones):
            flag = False

        for j in range(L):# Analizamos los vecinos superiores cercanos

            # Generamos los indicesde permutacion aleatoria
            it1 = it2 = rd.randint(0,len(ordenes)-1) 
            
            while(it1==it2):#Nos aseguramos que los indices sean distintos entre si
                it2 = rd.randint(0,len(ordenes)-1)
            permutacion_it = ordenes
            
            # Valores a permutar
            aux1, aux2 = ordenes[it1], ordenes[it2]
            
            # Hacemos el reemplazo de valores
            permutacion_it = ordenes
            permutacion_it[it1] = aux2
            permutacion_it[it2] = aux1
            #print(permutacion_it)        
            costo_it = costo_secuencia(permutacion_it, coor_Extremos,enumeracion) # Determinamos el costo del camino
            
            # Funciones del Temple
            delta = abs(costo_it - costo_optimo_rel)
            valor_random = rd.random()
            exponencial = math.exp(-(delta/t))
            
            # Probabilidad de encontrar la solucion
            if (valor_random<exponencial or delta<0):
                optima_permutacion_rel = permutacion_it
                costo_optimo_rel = costo_it

        #Actualizar Parametros
        t = alfa * t
        cant_repeticiones +=1
        it +=j

        # Si se obtuvo un mejor resultado, se almacena y se reinicia la cantidad de repiticiones
        if (costo_optimo_rel < costo_optimo):
            optima_permutacion = optima_permutacion_rel
            costo_optimo = costo_optimo_rel
            cant_repeticiones = 0
        
        #Mostrar resultado de cada iteracion    
        text = "Iteración: " + str(cont) + " - Costo óptimo:" + str(costo_optimo) + " - Temperatura: " + str(t)  + " - Permutaciones: " + str(it)
        print(text)

    optima_permutacion = ["Picking"] + optima_permutacion + ["Packing"]
    return costo_optimo, optima_permutacion




if __name__ == '__main__': #Para que se pueda usar sin interfaz grafica
    print("----------------TEMPLE SIMULADO----------------")
    print("Ingrese la secuencia de pedidos separado por una coma")
    #pedidos = input("Ordenes: ")
    pedidos ="5,17,25,12"
    print("Ingrese coordenadas del Picking, separada por coma")
    #picking = input("Coordenas x,y: ")
    picking = "0,0"
    print("Ingrese coordenadas del Packing, separada por coma")
    #packing = input("Coordenas x,y: ")
    packing = "1,4"
    
    #texto = "6, 38, 12, 67, 52, 43, 69, 61" # 75 - 52,6, 12, 69,67, 43, 61, 38
    #texto ="61,69,6,43,38,12"   # 53 - 69,38,61,6,12,43    
    #texto = "33,7,12,23" # 49
    
    cant_Filas, cant_columnas,espaciado_alto, alto, espaciado_ancho, ancho = Lab.ExtraccionDatos()
    cant_estantes = cant_Filas*cant_columnas*alto*ancho
    ###-----------------------
    ordenamiento = []
    # Asignar valores
    cont = 0
    for i in range(cant_estantes):
        cont+=1
        ordenamiento.append(cont)
    #print(ordenamiento)
    
    #costo_optimo, optima_permutacion, optima_ruta = Temple(pedidos, picking, packing, ordenamiento)
    #costo_optimo, optima_permutacion= Temple(pedidos, picking,packing, ordenamiento)
    costo_optimo, optima_permutacion= Temple(pedidos, picking,packing)

    # Calcule antes la distancia optima, pero me falta el camino a seguir

    # Resultados
    print("\n-----------------------")
    print("RESULTADOS:")
    print("\nCosto total del picking óptimo: ", costo_optimo)
    print("Ruta de picking óptima:", optima_permutacion)

















    
  