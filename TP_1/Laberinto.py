def ExtraccionDatos():
        # Extraer los objetos del txt
        with open("datos.txt") as archivo:
                for linea in archivo:
                        datos = linea.split(",")
                        datos.pop()
    
        # Variables
        #print(datos)
        cant_Filas = int(datos[0])
        cant_columnas =  int(datos[1])
        espaciado_alto = int(datos[2])
        alto =  int(datos[3])
        espaciado_ancho = int(datos[4])
        ancho = int(datos[5])

        return cant_Filas, cant_columnas,espaciado_alto, alto, espaciado_ancho, ancho 



def Mapa():
    # Definir el mapa del problema
    # Los 0 es por donde se puede pasar y los 1 por donde no se puede cruzar

        cant_Filas, cant_columnas,espaciado_alto, alto, espaciado_ancho, ancho = ExtraccionDatos()
        
        # Generar cada una de las listas correspondientes
        test = []
        # Creamos la matriz llena de ceros
        for i in range(cant_Filas*(espaciado_alto+alto)+espaciado_alto):
                filas =  []
                for j in range(cant_columnas*(espaciado_ancho+ancho)+espaciado_ancho):
                        filas.append(0)
                test.append(filas)
        
        cont = 0
        espaciado = 0
        # Rellenamos la matriz donde hay obstaculos
        for i in range(cant_Filas*(espaciado_alto+alto)): # Filas
                cont+=1 
                if(espaciado_alto<cont<=espaciado_alto+alto): # Vemos si esta dentro del rango de un grupo de filas

                        # Graficar por agrupacion de columnas
                        for g in range(cant_columnas):
                                espaciado = g*(ancho+espaciado_ancho) # Espaciado acumulado en y

                                # Evaluamos para cada agrupacion de columna
                                for j in range(ancho+espaciado_ancho):
                                        if(ancho<=j<ancho+espaciado_ancho):
                                                test[i][espaciado+j] = 1

                if(cont==(espaciado_alto+alto)): # Cuando ya alacance la altura + espaciado, alcanzo el borde del grupo y se reinicia
                        cont=0
        
       # Devolvemos la matriz de listas
        return test