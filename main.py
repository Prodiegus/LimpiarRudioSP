import importlib
import os

def mostrar_menu():
    print("Seleccione una opción:")
    print("1. Comparar imágenes")
    print("2. Contaminar imagen con ruido de sal y pimienta")
    print("3. Limpiar imagen de ruido paralelo")
    print("4  Limpiar imagen de ruido secuencial")
    print("5. Generar imagen sin ruido")
    print("6. Salir")

while True:
    mostrar_menu()
    opcion = input("Ingrese el número de la opción: ")

    if opcion == "1":
        os.system('clear')
        importlib.import_module('comparador').__init__
    elif opcion == "2":
        os.system('clear')
        importlib.import_module('contaminador').__init__
    elif opcion == "3":
        os.system('clear')
        importlib.import_module('limpiador').limpiar()
    elif opcion == "4":
        os.system('clear')
        importlib.import_module('noparalelo.limpiador').limpiar()
    elif opcion == "5":
        os.system('clear')
        importlib.import_module('generador').__init__
    elif opcion == "6":
        print("Saliendo del programa.")
        break
    else:
        print("Opción no válida. Intente nuevamente.")
