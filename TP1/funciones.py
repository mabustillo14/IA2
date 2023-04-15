import random
import matplotlib.pyplot as plt
from PIL import Image

def ordenar(lista):
    lista.sort(key=lambda x: x.f)
    return lista

def buscarProducto(Nodos, producto):
    for filas in Nodos:
        for elementos in filas:
            if elementos.nombre == producto:
                return([elementos.fila, elementos.columna])

def estadosVecinos(orden, _espacioBusqueda):
    subconjunto = []
    ordenAux = orden[:]
    i = 0
    stop=0
    while i < _espacioBusqueda:
        posA = random.randint(0, len(orden)-1)
        posB = random.randint(0, len(orden)-1)
        while posA == posB:
            posB = random.randint(0, len(orden)-1)
        ordenAux[posA], ordenAux[posB] = ordenAux[posB], ordenAux[posA]
        if ordenAux not in subconjunto:
            subconjunto.append(ordenAux[:])
            i += 1
        ordenAux = orden[:]
        if stop==5000:
            break
        stop+=1
    return subconjunto

def Graficar(Mapa, soluciones, titulo):
  # Cambiar valores a 0 y 1 para poder definir colores de pasillo y estante
  for i in range(len(Mapa)):
    fila = 0
    for j in range(len(Mapa[i])):
      if(Mapa[i][j] == " P"):
        Mapa[i][j] = 0 # Pasillo
      else: 
        Mapa[i][j] = 1 # Estante

  # Graficar los trayectos
  cont = 2
  for solucion in soluciones: # Graficamos cada solución
    for coordenada in solucion:
      Mapa[coordenada[0]][coordenada[1]] = cont
    cont += 1
  
  # Graficar los extremos de cada iniico
  plt.matshow(Mapa)

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
  path_img = './Mapa_solucion/'+ titulo +'.png'
  plt.savefig(path_img) 

  imagen_output = Image.open(path_img)
  return imagen_output
