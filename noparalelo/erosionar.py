import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm

class Erosionador:
    def __init__(self, estructura):
        self.estructura = estructura
        self.imagen = None
        self.imagen_erosionada = None

    def cargar_imagen(self, filepath):
        self.imagen = np.array(Image.open(filepath))

    def grey_erosion(self, imagen, estructura):
        # Obtener las dimensiones de la imagen y el elemento estructurante
        filas, columnas = imagen.shape[:2]
        ef, ec = estructura.shape

        # Crear una imagen de salida con ceros
        imagen_erosionada = np.zeros_like(imagen)

        # Calcular los offsets del elemento estructurante
        offset_filas = ef // 2
        offset_columnas = ec // 2

        pbar = tqdm(total=filas * columnas, desc="Aplicando erosión gris")

       # Aplicar erosión gris
        for i in range(filas):
            for j in range(columnas):
                # Obtener la región de la imagen que se superpone con el elemento estructurante
                region = imagen[max(i - offset_filas, 0):min(i + offset_filas + 1, filas),
                                max(j - offset_columnas, 0):min(j + offset_columnas + 1, columnas)]
                
                # Ajustar la región para que coincida con el tamaño del elemento estructurante
                region_padded = np.pad(region, ((max(0, offset_filas - i), max(0, (i + offset_filas + 1) - filas)),
                                                (max(0, offset_columnas - j), max(0, (j + offset_columnas + 1) - columnas))),
                                       mode='constant', constant_values=255)
                
                # Aplicar el elemento estructurante a la región
                min_valor = np.min(region_padded[:ef, :ec][estructura == 1])
                imagen_erosionada[i, j] = min_valor

                # Actualizar la barra de progreso
                pbar.update(1)
        pbar.close()
        return imagen_erosionada

    def aplicar_erosion(self, imagen):
        r, g, b = imagen[:,:,0], imagen[:,:,1], imagen[:,:,2]
        
        # Aplicar erosión a cada canal
        r_erosion = self.grey_erosion(r, self.estructura)
        g_erosion = self.grey_erosion(g, self.estructura)
        b_erosion = self.grey_erosion(b, self.estructura)
        
        imagen_erosionada = np.stack((r_erosion, g_erosion, b_erosion), axis=-1)
        return imagen_erosionada
    
    def aplicar_erosion(self, canal):
        canal_erosion = self.grey_erosion(canal, self.estructura)
        
        return canal_erosion
    
    def aplicar_erosion(self, imagen):
        r, g, b = imagen[:,:,0], imagen[:,:,1], imagen[:,:,2]
        
        # Aplicar erosión a cada canal
        r_erosion = self.grey_erosion(r, self.estructura)
        g_erosion = self.grey_erosion(g, self.estructura)
        b_erosion = self.grey_erosion(b, self.estructura)
        
        return np.stack((r_erosion, g_erosion, b_erosion), axis=-1)

    def obtener_imagen_erosionada(self):
        if self.imagen_erosionada is None:
            raise ValueError("No se ha aplicado la erosión a la imagen.")
        return self.imagen_erosionada

# Ejemplo de uso
if __name__ == '__main__':
    estructura = np.ones((3, 3))  # Elemento estructurante 3x3
    erosionador = Erosionador(estructura)
    
    # Cargar la imagen
    erosionador.cargar_imagen('ruta/a/tu/imagen.png')
    
    # Aplicar erosión
    erosionador.aplicar_erosion()
    
    # Obtener la imagen erosionada
    imagen_erosionada = erosionador.obtener_imagen_erosionada()
    
    # Guardar la imagen erosionada
    imagen_pil = Image.fromarray(imagen_erosionada.astype('uint8'))
    imagen_pil.save('imagen_erosionada.png')