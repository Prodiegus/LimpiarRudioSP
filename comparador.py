import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import os
import concurrent.futures

def comparar_imagen(imagen_original, imagen_completa_path):
    # Leer la imagen a comparar
    imagen_comparar = cv2.imread(imagen_completa_path, cv2.IMREAD_GRAYSCALE)
    if imagen_comparar is None:
        print(f"No se pudo leer la imagen {imagen_completa_path}")
        return imagen_completa_path, None

    # Redimensionar la imagen a comparar al tamaño de la imagen original
    imagen_comparar = cv2.resize(imagen_comparar, (imagen_original.shape[1], imagen_original.shape[0]))

    # Calcular la similitud usando SSIM
    score, _ = ssim(imagen_original, imagen_comparar, full=True)
    return imagen_completa_path, score * 100  # Convertir a porcentaje

def comparar_similitud(imagen_original_path, carpeta_imagenes):
    # Leer la imagen original
    imagen_original = cv2.imread(imagen_original_path, cv2.IMREAD_GRAYSCALE)
    if imagen_original is None:
        raise ValueError("No se pudo leer la imagen original")

    similitudes = []

    # Listar todos los archivos en la carpeta de imágenes
    imagenes_paths = [os.path.join(carpeta_imagenes, imagen_path) for imagen_path in os.listdir(carpeta_imagenes)]

    # Usar ThreadPoolExecutor para comparar las imágenes en paralelo
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futuros = [executor.submit(comparar_imagen, imagen_original, imagen_path) for imagen_path in imagenes_paths]
        for futuro in concurrent.futures.as_completed(futuros):
            imagen_path, similitud = futuro.result()
            if similitud is not None:
                similitudes.append((imagen_path, similitud))

    # Mostrar el porcentaje de similitud para cada imagen comparada
    for imagen_path, similitud in similitudes:
        print(f"Similitud con {imagen_path}: {similitud:.2f}%")
def imprimir_contenido_txt(ruta_archivo):
    try:
        with open(ruta_archivo, 'r') as archivo:
            contenido = archivo.read()
            print(contenido)
    except FileNotFoundError:
        print(f"El archivo {ruta_archivo} no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
# Ejemplo de uso
print("Comparando imágenes paralelas...")
comparar_similitud('pic.png', 'img')
imprimir_contenido_txt('tiempo_ejecucion.txt')
print("Comparando imágenes no paralelas...")
comparar_similitud('pic.png', 'noparalelo/img')
imprimir_contenido_txt('noparalelo/tiempo_ejecucion.txt')