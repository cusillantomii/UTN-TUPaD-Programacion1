"""TP 10: punto de entrada para los cinco ejercicios de POO."""

from entrada import leer_entero
from ejercicio_1_matriz.carga_matriz import main as cargar_matriz
from ejercicio_2_notas.carga_notas import CargaNotas
from ejercicio_3_restaurante.menu_restaurant import MenuRestaurant
from ejercicio_4_computadoras.costo_computadora import CostoComputadora
from ejercicio_5_barrio.demostracion_barrio import main as demostrar_barrio


def main():
    while True:
        print("\nTP 10 - PROGRAMACIÓN ORIENTADA A OBJETOS")
        print("1. Matriz y celdas")
        print("2. Alumnos y notas")
        print("3. Menú del restaurante")
        print("4. Cotización de computadoras")
        print("5. Barrio, viviendas y habitaciones (demostración)")
        print("0. Salir")
        opcion = leer_entero("Elegí un ejercicio: ")
        if opcion == 0:
            break
        elif opcion == 1:
            cargar_matriz()
        elif opcion == 2:
            CargaNotas.main()
        elif opcion == 3:
            MenuRestaurant.main()
        elif opcion == 4:
            CostoComputadora.main()
        elif opcion == 5:
            demostrar_barrio()
        else:
            print("Opción inválida. Elegí entre 0 y 5.")


if __name__ == "__main__":
    main()
