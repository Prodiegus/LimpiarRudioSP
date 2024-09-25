import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm

class Dilatador:
    def __init__(self, estructura):
        self.estructura = estructura
        self.imagen = None
        self.imagen_dilatada = None

    def cargar_imagen(self, filepath):
        self.imagen = np.array(Image.open(filepath))

    def grey_dilation(self, imagen, estructura):
        # Obtener las dimensiones de la imagen y el elemento estructurante
        filas, columnas = imagen.shape[:2]
        ef, ec = estructura.shape

        # Crear una imagen de salida con ceros
        imagen_dilatada = np.zeros_like(imagen)

        # Calcular los offsets del elemento estructurante
        offset_filas = ef // 2
        offset_columnas = ec // 2

        pbar = tqdm(total=filas * columnas, desc="Aplicando dilatación gris")

        # Aplicar dilatación gris
        for i in range(filas):
            for j in range(columnas):
                # Obtener la región de la imagen que se superpone con el elemento estructurante
                region = imagen[max(i - offset_filas, 0):min(i + offset_filas + 1, filas),
                                max(j - offset_columnas, 0):min(j + offset_columnas + 1, columnas)]
                
                # Ajustar la región para que coincida con el tamaño del elemento estructurante
                region_padded = np.pad(region, ((max(0, offset_filas - i), max(0, (i + offset_filas + 1) - filas)),
                                                (max(0, offset_columnas - j), max(0, (j + offset_columnas + 1) - columnas))),
                                       mode='constant', constant_values=0)
                
                # Aplicar el elemento estructurante a la región
                max_valor = np.max(region_padded * estructura)
                imagen_dilatada[i, j] = max_valor

                # Actualizar la barra de progreso
                pbar.update(1)
        pbar.close()
        return imagen_dilatada
    
    def aplicar_dilatacion(self):
        if self.imagen is None:
            raise ValueError("No se ha cargado ninguna imagen.")
        
        r, g, b = self.imagen[:,:,0], self.imagen[:,:,1], self.imagen[:,:,2]
        
        # Aplicar dilatación a cada canal
        r_dilatacion = self.grey_dilation(r, self.estructura)
        g_dilatacion = self.grey_dilation(g, self.estructura)
        b_dilatacion = self.grey_dilation(b, self.estructura)
        
        self.imagen_dilatada = np.stack((r_dilatacion, g_dilatacion, b_dilatacion), axis=-1)
        return self.imagen_dilatada
    
    def aplicar_dilatacion(self, canal):
        canal_dilatacion = self.grey_dilation(canal, self.estructura)
        
        return canal_dilatacion
    
    def aplicar_dilatacion(self, imagen):
        r, g, b = imagen[:,:,0], imagen[:,:,1], imagen[:,:,2]
        
        # Aplicar dilatación a cada canal
        r_dilatacion = self.grey_dilation(r, self.estructura)
        g_dilatacion = self.grey_dilation(g, self.estructura)
        b_dilatacion = self.grey_dilation(b, self.estructura)
        
        return np.stack((r_dilatacion, g_dilatacion, b_dilatacion), axis=-1)

    def obtener_imagen_dilatada(self):
        if self.imagen_dilatada is None:
            raise ValueError("No se ha aplicado la dilatación a la imagen.")
        return self.imagen_dilatada
    

# Ejemplo de uso
if __name__ == '__main__':
    estructura = np.ones((3, 3))  # Elemento estructurante 3x3
    dilatador = Dilatador(estructura)
    
    # Cargar la imagen
    dilatador.cargar_imagen('ruta/a/tu/imagen.png')
    
    # Aplicar dilatación
    dilatador.aplicar_dilatacion()
    
    # Obtener la imagen dilatada
    imagen_dilatada = dilatador.obtener_imagen_dilatada()
    
    # Guardar la imagen dilatada
    imagen_pil = Image.fromarray(imagen_dilatada.astype('uint8'))
    imagen_pil.save('imagen_dilatada.png')