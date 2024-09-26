import glob
import os
import time
import cv2
import numpy as np
from scipy.ndimage import grey_erosion, grey_dilation
from PIL import Image
from tqdm import tqdm
import threading
import multiprocessing as mp

# Cargar imagen en formato RGB
def cargar_imagen(filepath):
    return np.array(Image.open(filepath))

# Función para aplicar dilatacion a una parte de la imagen (multiprocessing)
def dilatacion_canal(canal, element, inicio_fila, fin_fila):
    sub_imagen = canal[inicio_fila:fin_fila, :]
    return cv2.dilate(sub_imagen, element, iterations=1)

# Función para aplicar erosión a una parte de la imagen (multiprocessing)
def erosion_canal(canal, element, inicio_fila, fin_fila):
    sub_imagen = canal[inicio_fila:fin_fila, :]
    return cv2.erode(sub_imagen, element, iterations=1)

# Función para aplicar erosión a una imagen completa (multiprocessing)
def erosionar_imagen(imagen, estructura):
    print("Erosionando la imagen")
    
    # Dividir los canales RGB
    r, g, b = imagen[:, :, 0], imagen[:, :, 1], imagen[:, :, 2]
    
    # Dividir la imagen en partes para el procesamiento paralelo
    alto_imagen = imagen.shape[0]
    particiones = 4  # Número de particiones/procesos
    alto_parte = alto_imagen // particiones
    
    canales = [r, g, b]
    imagen_erosionada = []
    tiempo_inicio = time.time()
    # Crear un pool de procesos
    with mp.Pool(processes=particiones) as pool:
        for canal in canales:
            resultados = []
            for i in range(particiones):
                inicio_fila = i * alto_parte
                fin_fila = (i + 1) * alto_parte if i != particiones - 1 else alto_imagen
                resultado = pool.apply_async(erosion_canal, args=(canal, estructura, inicio_fila, fin_fila))
                resultados.append(resultado)
            
            # Esperar a que todos los procesos terminen y recoger los resultados
            sub_imagenes_erosionadas = [res.get() for res in resultados]
            # Combinar las partes procesadas para formar el canal completo
            imagen_erosionada.append(np.vstack(sub_imagenes_erosionadas))

    # Combinar los canales erosionados nuevamente en una imagen RGB
    imagen_final = cv2.merge(imagen_erosionada)
    tiempo_final = time.time()
    tiempo_transcurrido = tiempo_final - tiempo_inicio
    with open('tiempo_erosion.txt', 'w') as archivo:
        if tiempo_transcurrido < 60:
            archivo.write(f"Tiempo de erosión: {tiempo_transcurrido:.2f} segundos\n")
        elif tiempo_transcurrido < 3600:
            minutos = int(tiempo_transcurrido // 60)
            segundos = tiempo_transcurrido % 60
            archivo.write(f"Tiempo de erosión: {minutos} minutos y {segundos:.2f} segundos\n")
        else:
            horas = int(tiempo_transcurrido // 3600)
            minutos = int((tiempo_transcurrido % 3600) // 60)
            segundos = tiempo_transcurrido % 3600
            archivo.write(f"Tiempo de erosión: {horas} horas, {minutos} minutos y {segundos:.2f} segundos\n")
    
    print("Erosión terminada")
    return imagen_final

def dilatar_imagen(imagen, estructura):
    print("Dilatando la imagen")
    
    # Dividir los canales RGB
    r, g, b = imagen[:, :, 0], imagen[:, :, 1], imagen[:, :, 2]
    
    # Dividir la imagen en partes para el procesamiento paralelo
    alto_imagen = imagen.shape[0]
    particiones = 4  # Número de particiones/procesos
    alto_parte = alto_imagen // particiones
    
    canales = [r, g, b]
    imagen_dilatada = []
    tiempo_inicio = time.time()
    # Crear un pool de procesos
    with mp.Pool(processes=particiones) as pool:
        for canal in canales:
            resultados = []
            for i in range(particiones):
                inicio_fila = i * alto_parte
                fin_fila = (i + 1) * alto_parte if i != particiones - 1 else alto_imagen
                resultado = pool.apply_async(dilatacion_canal, args=(canal, estructura, inicio_fila, fin_fila))
                resultados.append(resultado)
            
            # Esperar a que todos los procesos terminen y recoger los resultados
            sub_imagenes_dilatadas = [res.get() for res in resultados]
            # Combinar las partes procesadas para formar el canal completo
            imagen_dilatada.append(np.vstack(sub_imagenes_dilatadas))

    # Combinar los canales erosionados nuevamente en una imagen RGB
    imagen_final = cv2.merge(imagen_dilatada)
    tiempo_final = time.time()
    tiempo_transcurrido = tiempo_final - tiempo_inicio
    with open('tiempo_dilatacion.txt', 'w') as archivo:
        if tiempo_transcurrido < 60:
            archivo.write(f"Tiempo de dilatación: {tiempo_transcurrido:.2f} segundos\n")
        elif tiempo_transcurrido < 3600:
            minutos = int(tiempo_transcurrido // 60)
            segundos = tiempo_transcurrido % 60
            archivo.write(f"Tiempo de dilatación: {minutos} minutos y {segundos:.2f} segundos\n")
        else:
            horas = int(tiempo_transcurrido // 3600)
            minutos = int((tiempo_transcurrido % 3600) // 60)
            segundos = tiempo_transcurrido % 3600
            archivo.write(f"Tiempo de dilatación: {horas} horas, {minutos} minutos y {segundos:.2f} segundos\n")
    print("Dilatación terminada")
    return imagen_final

# Generar imagen sin ruido a partir de las imágenes erosionada y dilatada
def eliminar_ruido(imagen_erosionada, imagen_dilatada):
    # Combinar las imágenes tomando el promedio de ambas
    imagen_sin_ruido = (imagen_erosionada.astype(np.float32) + imagen_dilatada.astype(np.float32)) / 2
    return imagen_sin_ruido.astype(np.uint8)

# Guardar imagen en una carpeta
def guardar_imagen(imagen, nombre_archivo):
    if not os.path.exists('img'):
        os.makedirs('img')
    
    print(f"Guardando imagen '{nombre_archivo}.png'...")
    
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
def procesar_pimienta_parcial(imagen, inicio, fin, resultado, pbar):
    for i in range(inicio, fin):
        for j in range(imagen.shape[1]):
            if np.array_equal(imagen[i, j], [0, 0, 0]):
                resultado[i, j] = [255, 255, 255]
        pbar.update(1)

def quitar_pimienta(imagen):
    print("copiamos la imagen")
    imagen_sin_pimienta = imagen.copy()
    
    # Dividir la imagen en 10 porciones
    num_hilos = 6
    h, w, _ = imagen.shape
    porcion = h // num_hilos
    
    # Crear una lista para almacenar los resultados parciales
    resultado = imagen_sin_pimienta.copy()
    
    # Crear una barra de progreso
    pbar = tqdm(total=h, desc="Procesando filas (quitar pimienta)")
    
    # Crear hilos para procesar cada porción
    hilos = []
    for i in range(num_hilos):
        inicio = i * porcion
        fin = (i + 1) * porcion if i != num_hilos - 1 else h
        hilo = threading.Thread(target=procesar_pimienta_parcial, args=(imagen, inicio, fin, resultado, pbar))
        hilos.append(hilo)
    
    # Iniciar los hilos
    for hilo in hilos:
        hilo.start()
    
    # Esperar a que todos los hilos terminen
    for hilo in hilos:
        hilo.join()
    
    pbar.close()
    return resultado

def procesar_sal_parcial(imagen, inicio, fin, resultado, pbar):
    for i in range(inicio, fin):
        for j in range(imagen.shape[1]):
            if np.array_equal(imagen[i, j], [255, 255, 255]):
                resultado[i, j] = [0, 0, 0]
        pbar.update(1)

def quitar_sal(imagen):
    print("copiamos la imagen")
    imagen_sin_sal = imagen.copy()
    
    # Dividir la imagen en 10 porciones
    num_hilos = 10
    h, w, _ = imagen.shape
    porcion = h // num_hilos
    
    # Crear una lista para almacenar los resultados parciales
    resultado = imagen_sin_sal.copy()
    
    # Crear una barra de progreso
    pbar = tqdm(total=h, desc="Procesando filas (quitar sal)")
    
    # Crear hilos para procesar cada porción
    hilos = []
    for i in range(num_hilos):
        inicio = i * porcion
        fin = (i + 1) * porcion if i != num_hilos - 1 else h
        hilo = threading.Thread(target=procesar_sal_parcial, args=(imagen, inicio, fin, resultado, pbar))
        hilos.append(hilo)
    
    # Iniciar los hilos
    for hilo in hilos:
        hilo.start()
    
    # Esperar a que todos los hilos terminen
    for hilo in hilos:
        hilo.join()
    
    pbar.close()
    return resultado

def limpiar_pantalla():
    if os.name == 'nt':  # Para Windows
        os.system('cls')
    else:  # Para Linux y macOS
        os.system('clear')

def borrar_imagenes(directorio):
    # Obtener la lista de archivos en el directorio que tienen extensiones de imagen comunes
    imagenes = glob.glob(os.path.join(directorio, "*.png")) + \
               glob.glob(os.path.join(directorio, "*.jpg")) + \
               glob.glob(os.path.join(directorio, "*.jpeg")) + \
               glob.glob(os.path.join(directorio, "*.bmp")) + \
               glob.glob(os.path.join(directorio, "*.gif"))

    # Borrar cada archivo encontrado
    for imagen in imagenes:
        try:
            os.remove(imagen)
        except Exception as e:
            print(f"No se pudo borrar la imagen {imagen}: {e}")


def limpiar():    
    borrar_imagenes('img')
    imagen = cargar_imagen('imagen.png')
    elemento_estructurante = np.ones((3, 3))  # Elemento estructurante 3x3
    procesamiento = 4 # Número de veces que se aplicará erosión y dilatación

    # Limpiar la pantalla y avisar el inicio
    limpiar_pantalla()
    print("Iniciando la limpieza de la imagen sacando sal y pimienta...")

    tiempo_inicio = time.time()

    imagen_sin_sal = quitar_sal(imagen)
    print("\nimagen sin sal")
    imagen_sin_pimienta = quitar_pimienta(imagen)
    print("\nimagen sin pimienta")


    limpiar_pantalla()
    print("Iniciando erosion y dilatacion...")

    for i in range(procesamiento):
        imagen_erosionada = erosionar_imagen(imagen_sin_pimienta, elemento_estructurante)
        print("imagen erosionada: ", i)
        imagen_dilatada = dilatar_imagen(imagen_sin_sal, elemento_estructurante)
        print("imagen dilatada: ", i)
        #imagen_sin_sal = quitar_sal(imagen_erosionada)
        imagen_sin_sal = imagen_dilatada
        print("\nimagen sin sal: ", i)
        #imagen_sin_pimienta = quitar_pimienta(imagen_dilatada)
        imagen_sin_pimienta = imagen_erosionada
        print("\nimagen sin pimienta: ", i)

    limpiar_pantalla()
    print("quitando el ruido de la imagen...")
    # Eliminar ruido de la imagen
    imagen_sin_ruido = eliminar_ruido(imagen_erosionada, imagen_dilatada)

    tiempo_fin = time.time()

    # Guardar todas las versiones de la imagen
    print("Guardando imágenes del proceso...")
    guardar_imagen(imagen, 'imagen_original')
    guardar_imagen(imagen_sin_sal, 'imagen_sin_sal')
    guardar_imagen(imagen_sin_pimienta, 'imagen_sin_pimienta')
    guardar_imagen(imagen_erosionada, 'imagen_erosionada')
    guardar_imagen(imagen_dilatada, 'imagen_dilatada')
    guardar_imagen(imagen_sin_ruido, 'imagen_sin_ruido')

    print("Imágenes del proceso guardadas en la carpeta 'img'.")

    tiempo_transcurrido = tiempo_fin - tiempo_inicio
    if tiempo_transcurrido < 60:
        print(f"Tiempo transcurrido: {tiempo_transcurrido:.2f} segundos")
    elif tiempo_transcurrido < 3600:
        minutos = int(tiempo_transcurrido // 60)
        segundos = tiempo_transcurrido % 60
        print(f"Tiempo transcurrido: {minutos} minutos y {segundos:.2f} segundos")
    else:
        horas = int(tiempo_transcurrido // 3600)
        minutos = int((tiempo_transcurrido % 3600) // 60)
        segundos = tiempo_transcurrido % 60
        print(f"Tiempo transcurrido: {horas} horas, {minutos} minutos y {segundos:.2f} segundos")

    with open('tiempo_ejecucion.txt', 'w') as archivo:
        if tiempo_transcurrido < 60:
            archivo.write(f"Tiempo total de limpieza: {tiempo_transcurrido:.2f} segundos\n")
        elif tiempo_transcurrido < 3600:
            archivo.write(f"Tiempo total de limpieza: {minutos} minutos y {segundos:.2f} segundos\n")
        else:
            archivo.write(f"Tiempo total de limpieza: {horas} horas, {minutos} minutos y {segundos:.2f} segundos\n")
