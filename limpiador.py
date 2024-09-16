import os
import cv2
import numpy as np
from scipy.ndimage import grey_erosion, grey_dilation
from PIL import Image

# Cargar imagen en formato RGB
def cargar_imagen(filepath):
    return np.array(Image.open(filepath))

# Aplicar Erosión a cada canal de la imagen
def erosionar_imagen(imagen, estructura):
    r, g, b = imagen[:,:,0], imagen[:,:,1], imagen[:,:,2]
    # se hace un hilo para cada canal de la imagen
    r_erosion = grey_erosion(r, footprint=estructura)
    g_erosion = grey_erosion(g, footprint=estructura)
    b_erosion = grey_erosion(b, footprint=estructura)
    return np.stack((r_erosion, g_erosion, b_erosion), axis=-1)

# Aplicar Dilatación a cada canal de la imagen
def dilatar_imagen(imagen, estructura):
    r, g, b = imagen[:,:,0], imagen[:,:,1], imagen[:,:,2]
    r_dilatacion = grey_dilation(r, footprint=estructura)
    g_dilatacion = grey_dilation(g, footprint=estructura)
    b_dilatacion = grey_dilation(b, footprint=estructura)
    return np.stack((r_dilatacion, g_dilatacion, b_dilatacion), axis=-1)

# Generar imagen sin ruido a partir de las imágenes erosionada y dilatada
def eliminar_ruido(imagen_erosionada, imagen_dilatada):
    # Combinar las imágenes tomando el promedio de ambas
    imagen_sin_ruido = (imagen_erosionada.astype(np.float32) + imagen_dilatada.astype(np.float32)) / 2
    return imagen_sin_ruido.astype(np.uint8)

# Guardar imagen en una carpeta
def guardar_imagen(imagen, nombre_archivo):
    if not os.path.exists('img'):
        os.makedirs('img')
    
    imagen_pil = Image.fromarray(imagen.astype('uint8'))
    imagen_pil.save(f'img/{nombre_archivo}.png')

# ajustar la intensidad de los pixeles
def ajustar_imagen(imagen, factor):
    imagen = np.clip(imagen*factor, 0, 255)
    return imagen

# ajustamos el rgb de la imagen
def ajustar_colores_rgb(imagen):
    # Crear una copia de la imagen para no modificar la original
    imagen_ajustada = imagen.copy()
    
    # Recorrer cada píxel de la imagen
    for i in range(imagen.shape[0]):
        for j in range(imagen.shape[1]):
            # Obtener los valores RGB del píxel
            r, g, b = imagen[i, j]
            
            # Ajustar los valores RGB para mantener el más alto
            max_valor = max(r, g, b)
            imagen_ajustada[i, j] = [max_valor, max_valor, max_valor]
    
    return imagen_ajustada

# saturar la imagen
def incrementar_saturacion(imagen, factor):
    # Asegurarse de que la imagen esté en formato CV_8U
    if imagen.dtype != np.uint8:
        imagen = (imagen * 255).astype(np.uint8)
    
    # Convertir la imagen de RGB a HSV
    imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_RGB2HSV)
    
    # Incrementar el canal de saturación
    imagen_hsv[:, :, 1] = np.clip(imagen_hsv[:, :, 1] * factor, 0, 255)
    
    # Convertir la imagen de nuevo a RGB
    imagen_rgb = cv2.cvtColor(imagen_hsv, cv2.COLOR_HSV2RGB)
    
    return imagen_rgb

# quitar la pimienta de la imagen
def quitar_pimienta(imagen):
    # Crear una copia de la imagen para no modificar la original
    imagen_sin_pimienta = imagen.copy()
    
    # Recorrer cada píxel de la imagen
    for i in range(imagen.shape[0]):
        for j in range(imagen.shape[1]):
            # Verificar si el píxel es negro
            if np.array_equal(imagen[i, j], [0, 0, 0]):
                # Cambiar el píxel a blanco
                imagen_sin_pimienta[i, j] = [255, 255, 255]
    
    return imagen_sin_pimienta

# quitar sal de la imagen
def quitar_sal(imagen):
    # Crear una copia de la imagen para no modificar la original
    imagen_sin_sal = imagen.copy()
    
    # Recorrer cada píxel de la imagen
    for i in range(imagen.shape[0]):
        for j in range(imagen.shape[1]):
            # Verificar si el píxel es blanco
            if np.array_equal(imagen[i, j], [255, 255, 255]):
                # Cambiar el píxel a negro
                imagen_sin_sal[i, j] = [0, 0, 0]
    
    return imagen_sin_sal


# Ejemplo de uso
if __name__ == '__main__':
    imagen = cargar_imagen('imagen.png')
    elemento_estructurante = np.ones((3, 3))  # Elemento estructurante 3x3
    procesamiento = 5

    imagen_sin_sal = quitar_sal(imagen)
    imagen_sin_pimienta = quitar_pimienta(imagen)

    for i in range(procesamiento):
        imagen_erosionada = erosionar_imagen(imagen_sin_pimienta, elemento_estructurante)
        imagen_dilatada = dilatar_imagen(imagen_sin_sal, elemento_estructurante)
        imagen_sin_sal = quitar_sal(imagen_erosionada)
        imagen_sin_pimienta = quitar_pimienta(imagen_dilatada)

    # Ajustar la intensidad de los pixeles
    factor_ajuste = 0.8
    imagen_ajustada = ajustar_imagen(imagen, factor_ajuste)

    # Ajustar los colores RGB de la imagen
    imagen_ajustada_rgb = ajustar_colores_rgb(imagen_ajustada)

    # Incrementar la saturación de la imagen
    factor_saturacion = 1.5
    imagen_saturada = incrementar_saturacion(imagen_ajustada_rgb, factor_saturacion)

    # Eliminar ruido de la imagen
    imagen_sin_ruido = eliminar_ruido(imagen_erosionada, imagen_dilatada)

    # Guardar todas las versiones de la imagen
    guardar_imagen(imagen, 'imagen_original')
    guardar_imagen(imagen_sin_sal, 'imagen_sin_sal')
    guardar_imagen(imagen_sin_pimienta, 'imagen_sin_pimienta')
    guardar_imagen(imagen_erosionada, 'imagen_erosionada')
    guardar_imagen(imagen_dilatada, 'imagen_dilatada')
    guardar_imagen(imagen_ajustada, 'imagen_ajustada')
    guardar_imagen(imagen_ajustada_rgb, 'imagen_ajustada_rgb')
    guardar_imagen(imagen_saturada, 'imagen_saturada')
    guardar_imagen(imagen_sin_ruido, 'imagen_sin_ruido')

    print("Imágenes del proceso guardadas en la carpeta 'img'.")
