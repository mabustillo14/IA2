"""
GUI: Graphical User Interface
Hacemos uso de Gradio: pip3 install gradio
"""

import gradio as gr
from A_estrella import solucion, MostrarMapa, DeterminarCoordenadas
from temple import Temple
import Laberinto as Lab


cant_Filas, cant_columnas,espaciado_alto, alto, espaciado_ancho, ancho = Lab.ExtraccionDatos()

# Obtener caracteristicas del Laberinto
maze = Lab.Mapa()
cant_estantes = alto*ancho*cant_columnas*cant_Filas

# Mostar el Mapa por pantalla
MostrarMapa('mapa.png','Mapa', maze)

# Descripción del Header
title = "Resolución de Lista de Pedidos 🗺️"
description = '**Input:** Lista de orden de pedidos, separado cada pedido por una coma.<br>' 
description += '**Output:** Secuencia óptima, Path óptimo , Mapa con la solución <br>'
description += '**Características:** El Laberinto tiene '  + str(cant_estantes) +' estantes disponibles'

# Descripción del Footer
article = '**Desafío:** El robot debe transportar cajas desde distintos estantes de la manera de menor coste total a través de un laberinto predefinido, utilizando el algoritmo de Temple Simulado.<br> '
article += '**Mario Bustillo 2023 🚀** | [Github](https://github.com/mabustillo14) | [Linkedin](https://www.linkedin.com/in/mario-bustillo/) 🤗 '
enable_queue=False

# Entrada de datos
text1 = gr.Textbox(label="Mesa Inicial") # Ordenes

# Salida de datos
text2 = gr.Textbox(label="Costo del picking óptimo")
text3 = gr.Textbox(label="Secuencia de picking óptima")
text4 = gr.Textbox(label="Ruta Solución óptima")
image1 = gr.Image(shape=(140, 140), label="Mapa Solución")

# Ejemplos
examples = [["5, 25, 33,15"]]

# Planteamiento de la Interfaz
demo = gr.Interface(
    fn=Temple, 
    inputs=[text1], 
    outputs=[text2,text3,text4,image1],
    title=title,
    description=description,
    article=article, 
    examples = examples
    )
demo.launch(enable_queue=enable_queue,debug=True)

