from temp import Temple
import Laberinto as Lab


# Aca paso el numero del pedido y el estante donde se encuentra

ordenes ="91,108,83,96"
picking = "0,0"
packing = "1,4"

###-----------------------
ordenes = ordenes.split(",")
print(ordenes)
###-----------------------
cant_Filas, cant_columnas,espaciado_alto, alto, espaciado_ancho, ancho = Lab.ExtraccionDatos()
cant_estantes = cant_Filas*cant_columnas*alto*ancho
###-----------------------

#Nuevo ordenamiento
ordenamiento = []
# Asignar valores
cont = 0
for i in range(cant_estantes):
    ordenamiento.append(cant_estantes-i)
print(ordenamiento)


ordenamiento2 = []
# Asignar valores
cont = 0
for i in range(1,cant_estantes+1):
    ordenamiento2.append(i)
print(ordenamiento2)
print(len(ordenamiento2))





pedidos_referidos=""
# Debo referenciar los pedidos a la numeracion original
for j in range(len(ordenes)-1):
    ordenes[j] = int(ordenes[j])
    print(ordenes[j])

    for i in range(len(ordenamiento)):
        
        if(ordenes[j] == ordenamiento[i]):
            pedidos_referidos += str(ordenamiento2[i]) + ","
            

cont = 0
for i in range(len(ordenamiento)):
    
    if(int(ordenes[len(ordenes)-1]) == ordenamiento[i]):
        pedidos_referidos += str(cont) 
    cont += 1    
        
        


print(pedidos_referidos)


costo_optimo, optima_permutacion = Temple(pedidos_referidos, picking,packing)

print(costo_optimo)
print(optima_permutacion)
