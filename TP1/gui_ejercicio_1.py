"""
GUI: Graphical User Interface
Hacemos uso de Gradio: pip3 install gradio
"""

import gradio as gr
from A_ESTRELLA import GUI


# Descripción del Header
title = "Resolución de Laberinto 🗺️"
description = '**Input:** Ingresar estante inicial y objetivo.<br>' 
description += '**Output:** Path , Mapa con la solución <br>'
#description += '**Características:** El Laberinto tiene '  + str(cant_estantes) +' estantes disponibles'

# Descripción del Footer
article = '**Desafío:** El robot debe transportar cajas desde un esstante  A a un estante B a través de un laberinto predefinido, utilizando el algoritmo A*.<br> '
article += '**Mario Bustillo 2023 🚀** | [Github](https://github.com/mabustillo14) | [Linkedin](https://www.linkedin.com/in/mario-bustillo/) 🤗 '
enable_queue=False

# Entrada de datos
text1 = gr.Textbox(label="Ingrese coordenada X del inicio (FILA) (Entrada al almacén):") #Ax
text2 = gr.Textbox(label="Ingrese coordenada Y del inicio (COLUMNA)(Entrada al almacén):") #Ay

text3 = gr.Textbox(label="Ingrese coordenada X de la meta (FILA) (Producto a buscar):") #Bx
text4 = gr.Textbox(label="Ingrese coordenada Y de la meta (COLUMNA) (Producto a buscar):") #By


# Salida de datos
text5 = gr.Textbox(label="Costo del camino")
text6 = gr.Textbox(label="Secuencia Solución")
image1 = gr.Image(shape=(140, 140), label="Mapa Solución")


# Planteamiento de la Interfaz
demo = gr.Interface(
    fn=GUI, 
    inputs=[text1, text2, text3, text4], 
    outputs=[text5,text6, image1],
    title=title,
    description=description,
    article=article
    )
demo.launch(enable_queue=enable_queue,debug=True)

