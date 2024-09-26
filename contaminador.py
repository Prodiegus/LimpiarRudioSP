import cv2
import numpy as np

def agregar_ruido_sal_pimienta(imagen_path, porcentaje_ruido, salida_path):
    # Leer la imagen
    imagen = cv2.imread(imagen_path, cv2.IMREAD_COLOR)
    if imagen is None:
        raise ValueError("No se pudo leer la imagen")

    # Calcular el número de píxeles que se verán afectados por el ruido
    num_pixeles = imagen.shape[0] * imagen.shape[1]
    num_ruido = int(porcentaje_ruido * num_pixeles)

    # Generar coordenadas aleatorias para los píxeles que se verán afectados
    pimienta_coords = [np.random.randint(0, i - 1, num_ruido) for i in imagen.shape]
    sal_coords = [np.random.randint(0, i - 1, num_ruido) for i in imagen.shape]


    # Asignar valores de 0 (sal) y 255 (pimienta) a los píxeles seleccionados
    imagen[pimienta_coords[0], pimienta_coords[1], :] = 255
    imagen[sal_coords[0], sal_coords[1], :] = 0

    # Guardar la imagen resultante
    cv2.imwrite(salida_path, imagen)

# Ejemplo de uso
def contaminar():
    ruta = input("Ingrese la ruta de la imagen: ")
    porcentaje = float(input("Ingrese el porcentaje de ruido: "))
    agregar_ruido_sal_pimienta(ruta, porcentaje, 'imagen.png')