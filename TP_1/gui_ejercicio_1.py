"""
GUI: Graphical User Interface
Hacemos uso de Gradio: pip3 install gradio
"""

import gradio as gr
from A_estrella import solucion, MostrarMapa, DeterminarCoordenadas
import Laberinto as Lab


cant_Filas, cant_columnas,espaciado_alto, alto, espaciado_ancho, ancho = Lab.ExtraccionDatos()

# Obtener caracteristicas del Laberinto
maze = Lab.Mapa()
cant_estantes = alto*ancho*cant_columnas*cant_Filas

# Mostar el Mapa por pantalla
MostrarMapa('mapa.png','Mapa', maze)

# Descripción del Header
title = "Resolución de Laberinto 🗺️"
description = '**Input:** Ingresar estante inicial y objetivo.<br>' 
description += '**Output:** Path , Mapa con la solución <br>'
description += '**Características:** El Laberinto tiene '  + str(cant_estantes) +' estantes disponibles'

# Descripción del Footer
article = '**Desafío:** El robot debe transportar cajas desde un esstante  A a un estante B a través de un laberinto predefinido, utilizando el algoritmo A*.<br> '
article += '**Mario Bustillo 2023 🚀** | [Github](https://github.com/mabustillo14) | [Linkedin](https://www.linkedin.com/in/mario-bustillo/) 🤗 '
enable_queue=False

# Entrada de datos
text1 = gr.Textbox(label="Mesa Inicial") #A
text2 = gr.Textbox(label="Mesa Objetivo") #B

# Salida de datos
text5 = gr.Textbox(label="Secuencia Solución")
image1 = gr.Image(shape=(140, 140), label="Mapa Solución")

# Ejemplos
examples = [[23,43]]

# Planteamiento de la Interfaz
demo = gr.Interface(
    fn=solucion, 
    inputs=[text1, text2], 
    outputs=[text5,image1],
    title=title,
    description=description,
    article=article, 
    examples = examples
    )
demo.launch(enable_queue=enable_queue,debug=True)

