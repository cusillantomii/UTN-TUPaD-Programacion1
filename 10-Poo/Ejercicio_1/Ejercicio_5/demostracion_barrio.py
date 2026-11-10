from .barrio import Barrio
from .habitacion import Habitacion
from .vivienda import Vivienda


class DemostracionBarrio:
    @staticmethod
    def main():
        barrio = Barrio("Los Aromos", "Constructora Sur")
        vivienda_1 = Vivienda("San Martín", 100, "A", 1, 200)
        vivienda_1.agregar_habitacion(Habitacion("Cocina", 30))
        vivienda_1.agregar_habitacion(Habitacion("Dormitorio", 20))
        vivienda_2 = Vivienda("Belgrano", 200, "B", 2, 150)
        vivienda_2.agregar_habitacion(Habitacion("Comedor", 25))
        vivienda_2.agregar_habitacion(Habitacion("Dormitorio", 15))
        barrio.agregar_vivienda(vivienda_1)
        barrio.agregar_vivienda(vivienda_2)

        print(f"\nBarrio: {barrio.nombre} | Constructora: {barrio.empresaConstructora}")
        print(f"Terreno total: {barrio.getSuperficieTotalTerreno():.2f} m²")
        print(f"Terreno de manzana A: {barrio.getSuperficieTotalTerrenoXManzana('A'):.2f} m²")
        print(f"Terreno de manzana B: {barrio.getSuperficieTotalTerrenoXManzana('B'):.2f} m²")
        for vivienda in barrio.viviendas:
            print(f"Casa {vivienda.nroCasa}: {vivienda.getMetrosCuadradosCubiertos():.2f} m² cubiertos")
        print(f"Superficie cubierta del barrio: {barrio.getSuperficieTotalCubierta():.2f} m²")

        # Caso de error separado: esta vivienda no se agrega al barrio válido.
        vivienda_invalida = Vivienda("Prueba", 1, "C", 3, 20)
        vivienda_invalida.agregar_habitacion(Habitacion("Habitación demasiado grande", 25))
        try:
            vivienda_invalida.getMetrosCuadradosCubiertos()
        except ValueError as error:
            print(f"Validación esperada: {error}")


def main():
    DemostracionBarrio.main()
