import os
from ollama import chat
from ollama import ChatResponse
from PyPDF2 import PdfReader

modelo = "qwen2:1.5b"




def renombrador(archivo):
    reader = PdfReader(archivo)
    page = reader.pages[0]
    text = page.extract_text()

    stream = chat(
        model=modelo,
        messages=[{'role': 'user',
                   'content': f'Propón un único nombre técnico y estructurado para titular un archivo PDF académico, basado en el siguiente extracto: {text}. El nombre debe ser claro, conciso y específico, similar a “Clase 1.1 Cálculo”. Usa un estilo formal, ordenado y orientado a cursos o documentos académicos. No incluyas explicaciones ni comillas. Entrega solo el nombre, en una línea. No seas estupido, no cometas errores'}],
        stream=True,
    )

    nuevo_nombre = ""
    for chunk in stream:
        nuevo_nombre += chunk['message']["content"]

    return nuevo_nombre


def seleccion(archivo):
    lista = []
    for _ in range(0,8):
        lista.append(renombrador(archivo))

    print(lista)
    stream = chat(
        model=modelo,
        messages=[{'role': 'user',
                   'content': f'Elige el mejor título de la siguiente lista, aquel que describa con mayor precisión el contenido del archivo y que, al mismo tiempo, facilite su organización en el computador. El archivo es: {archivo}. Los títulos son: {lista}. Entrega únicamente el título seleccionado, sin explicación, en una sola línea. No uses comillas ni texto adicional. No seas estupido, no cometas errores.'}],
        stream=True,
    )

    final = ""
    for chunk in stream:
        final += chunk['message']["content"]

    return final






