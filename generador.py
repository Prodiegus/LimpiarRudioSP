import cv2
import numpy as np
import random

def generar_imagen(n, m, salida_path):
    # Crear una imagen con un fondo de color aleatorio
    fondo_color = [random.randint(0, 255) for _ in range(3)]
    imagen = np.full((m, n, 3), fondo_color, dtype=np.uint8)

    # Calcular el tamaño máximo de las figuras geométricas
    tamano_figura = min(n, m)/5

    # Generar una secuencia aleatoria de figuras geométricas
    for _ in range(10):  # Número de figuras a dibujar
        figura = random.choice(['circulo', 'rectangulo', 'triangulo'])
        color_figura = [random.randint(0, 255) for _ in range(3)]
        if figura == 'circulo':
            centro = (random.randint(0, n-1), random.randint(0, m-1))
            radio = random.randint(1, tamano_figura)
            cv2.circle(imagen, centro, radio, color_figura, -1)
        elif figura == 'rectangulo':
            esquina1 = (random.randint(0, n-1), random.randint(0, m-1))
            esquina2 = (random.randint(esquina1[0], min(esquina1[0] + int(tamano_figura), n-1)),
                        random.randint(esquina1[1], min(esquina1[1] + int(tamano_figura), m-1)))
            cv2.rectangle(imagen, esquina1, esquina2, color_figura, -1)
        elif figura == 'triangulo':
            p1 = (random.randint(0, n-1), random.randint(0, m-1))
            p2 = (random.randint(0, n-1), random.randint(0, m-1))
            p3 = (random.randint(0, n-1), random.randint(0, m-1))
            pts = np.array([p1, p2, p3], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.fillPoly(imagen, [pts], color_figura)

    # Guardar la imagen resultante
    cv2.imwrite(salida_path, imagen)

# Ejemplo de uso
tamaño = int(input("Ingrese el tamaño de la imagen x: "))
altura = int(input("Ingrese el tamaño de la imagen y: "))
generar_imagen(tamaño, altura, 'pic.png')
print("Imagen generada con éxito.")
