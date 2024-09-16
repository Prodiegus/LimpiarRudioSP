import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import os

def comparar_similitud(imagen_original_path, carpeta_imagenes):
    # Leer la imagen original
    imagen_original = cv2.imread(imagen_original_path, cv2.IMREAD_GRAYSCALE)
    if imagen_original is None:
        raise ValueError("No se pudo leer la imagen original")

    similitudes = []

    # Listar todos los archivos en la carpeta de imágenes
    for imagen_path in os.listdir(carpeta_imagenes):
        imagen_completa_path = os.path.join(carpeta_imagenes, imagen_path)
        
        # Leer la imagen a comparar
        imagen_comparar = cv2.imread(imagen_completa_path, cv2.IMREAD_GRAYSCALE)
        if imagen_comparar is None:
            print(f"No se pudo leer la imagen {imagen_completa_path}")
            continue

        # Redimensionar la imagen a comparar al tamaño de la imagen original
        imagen_comparar = cv2.resize(imagen_comparar, (imagen_original.shape[1], imagen_original.shape[0]))

        # Calcular la similitud usando SSIM
        score, _ = ssim(imagen_original, imagen_comparar, full=True)
        similitudes.append((imagen_completa_path, score * 100))  # Convertir a porcentaje

    # Mostrar el porcentaje de similitud para cada imagen comparada
    for imagen_path, similitud in similitudes:
        print(f"Similitud con {imagen_path}: {similitud:.2f}%")

# Ejemplo de uso
comparar_similitud('pic.png', 'img')