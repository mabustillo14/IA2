import Laberinto as Lab
from A_estrella import solucionAstar

def Calcular_distancias():
    cant_Filas, cant_columnas,espaciado_alto, alto, espaciado_ancho, ancho = Lab.ExtraccionDatos()
    index = cant_Filas * cant_columnas * alto * ancho 

    #Relleno con la distancia a cada una de ellas
    Inicio = 1
    Fin = 30

    while(Inicio<=Fin):
        medidas = str(Inicio) + ","
        for i in range(1, Fin-1): 
            dist = len(solucionAstar(Inicio, i)) -1    
            print("Calculado distancia", Inicio, "a" ,i, "es", dist)
            medidas += str(dist) + ","
        dist = len(solucionAstar(Inicio, Fin)) -1
        medidas += str(dist) + ",\n"

        with open("mediciones.txt","a") as file:
            file.write(medidas)
        Inicio += 1


if __name__ == '__main__': #Para que se pueda usar sin interfaz grafica
    #print(Extraer_Distancias()) # Se introduce estante inicial y estante objetivo para obtener la distancia
    Calcular_distancias()