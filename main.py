import os
import sys
import subprocess
import importlib
import time

import numpy as np

def mostrar_menu():
    print("1. Comparar")
    print("2. Contaminar")
    print("3. Limpiar")
    print("4. Limpiar (sin paralelo)")
    print("5. Generar")
    print("6. Salir")

def limpiar_pantalla():
    if os.name == 'nt':  # Para Windows
        os.system('cls')
    else:  # Para Linux y macOS
        os.system('clear')
        
# Lista de dependencias necesarias
dependencias = {
    "opencv-python": "cv2",
    "numpy": "numpy",
    "scipy": "scipy",
    "pillow": "PIL",
    "tqdm": "tqdm"
}

def instalar_pip():
    print("Instalando pip...")
    subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])

def instalar_dependencias():
    for paquete in dependencias:
        try:
            __import__(paquete)
        except ImportError:
            print(f"Instalando {paquete}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])

def verificar_e_instalar():
    print("Verificando dependencias...")
    try:
        import pip
        print("pip ya está instalado.")
    except ImportError:
        instalar_pip()
    instalar_dependencias()
    
def print_estructurante(estructurante):
    for i in range(estructurante.shape[0]):
        for j in range(estructurante.shape[1]):
            if estructurante[i, j] == 1:
                print("■", end=" ")
            else:
                print(" ", end=" ")
        print() 
    
def get_estructurante():
    l = np.zeros((2, 2), dtype=np.uint8)
    vertical = np.zeros((2, 1), dtype=np.uint8)
    x = np.zeros((3, 3), dtype=np.uint8)
    horizontal = np.zeros((1, 3), dtype=np.uint8)
    l_invertida = np.zeros((2, 2), dtype=np.uint8)
    
    l[0:2, 1] = 1  # Columna derecha
    l[1, 0] = 1    # Fila inferior, segundo elemento
    
    horizontal[0, 0:3] = 1
    
    vertical[0, 0] = 1
    vertical[1, 0] = 1
    
    l_invertida[0, 0:1] = 1    # Columna izquierda
    l_invertida[0:2, 1] = 1     # Fila inferior, segundo elemento
    
    np.fill_diagonal(x, 1)      # Diagonal principal
    np.fill_diagonal(np.fliplr(x), 1)  # Diagonal secundaria
    
    while True:
        limpiar_pantalla()
        print("Menú de selección de elemento estructurante")
        print("1. elemento estructurante con forma de L invertida")
        print_estructurante(l_invertida)
        print("2. elemento estructurante con forma de L")
        print_estructurante(l)
        print("3. elemento estructurante con forma horizontal")
        print_estructurante(horizontal)
        print("4. elemento estructurante con forma de vertical")
        print_estructurante(vertical)
        print("5. elemento estructurante con forma de X")
        print_estructurante(x)
        
        opcion = int(input("Ingrese el número de la opción: "))
        
        if opcion == 1:
            return l_invertida
        elif opcion == 2:
            return l
        elif opcion == 3:
            return horizontal
        elif opcion == 4:
            return vertical
        elif opcion == 5:
            return x
        else:
            print("Opción no válida. Intente nuevamente.")
            time.sleep(0.5)
    


verificar_e_instalar()
limpiar_pantalla()
while True:
    mostrar_menu()
    opcion = input("Ingrese el número de la opción: ")

    if opcion == "1":
        limpiar_pantalla()
        importlib.import_module('comparador').comparar()
    elif opcion == "2":
        limpiar_pantalla()
        importlib.import_module('contaminador').contaminar()
    elif opcion == "3":
        limpiar_pantalla()
        importlib.import_module('limpiador').limpiar(get_estructurante(), int(input("Cuantas veces procesará la imagen: "))) 
    elif opcion == "4":
        limpiar_pantalla()
        importlib.import_module('noparalelo.limpiador').limpiar(get_estructurante(), int(input("Cuantas veces procesará la imagen: ")))
    elif opcion == "5":
        limpiar_pantalla()
        importlib.import_module('generador').generar()
    elif opcion == "6":
        print("Saliendo del programa.")
        break
    else:
        print("Opción no válida. Intente nuevamente.")