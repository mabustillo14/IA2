def def_Mapa():
    Mapa = []
    # Extraer los objetos del txt
    with open("Mapa.txt") as archivo:
            for linea in archivo:
                    datos = linea.split(",")
                    datos.pop(len(datos)-1)
                    Mapa.append(datos)

    return Mapa