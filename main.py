import os
import importlib

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

print("6. Salir")

while True:
    mostrar_menu()
    opcion = input("Ingrese el número de la opción: ")

    if opcion == "1":
        limpiar_pantalla()
        importlib.import_module('comparador').__init__
    elif opcion == "2":
        limpiar_pantalla()
        importlib.import_module('contaminador').__init__
    elif opcion == "3":
        limpiar_pantalla()
        importlib.import_module('limpiador').limpiar()
    elif opcion == "4":
        limpiar_pantalla()
        importlib.import_module('noparalelo.limpiador').limpiar()
    elif opcion == "5":
        limpiar_pantalla()
        importlib.import_module('generador').__init__
    elif opcion == "6":
        print("Saliendo del programa.")
        break
    else:
        print("Opción no válida. Intente nuevamente.")