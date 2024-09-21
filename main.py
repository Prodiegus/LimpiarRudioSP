import importlib

def mostrar_menu():
    print("Seleccione una opción:")
    print("1. Comparar imágenes")
    print("2. Contaminar imagen con ruido de sal y pimienta")
    print("3. Limpiar imagen de ruido")
    print("4. Generar imagen sin ruido")
    print("5. Salir")

while True:
    mostrar_menu()
    opcion = input("Ingrese el número de la opción: ")

    if opcion == "1":
        comparador = importlib.import_module('comparador')
        comparador  # Este módulo se cargará en este punto
    elif opcion == "2":
        contaminador = importlib.import_module('contaminador')
        contaminador  # Este módulo se cargará aquí
    elif opcion == "3":
        limpiador = importlib.import_module('limpiador')
        limpiador  # Este módulo se cargará aquí
    elif opcion == "4":
        generador = importlib.import_module('generador')
        generador  # Este módulo se cargará aquí
    elif opcion == "5":
        print("Saliendo del programa.")
        break
    else:
        print("Opción no válida. Intente nuevamente.")
