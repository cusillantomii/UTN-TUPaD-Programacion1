from entrada import confirmar, leer_decimal, leer_texto
from .ingrediente import Ingrediente
from .plato import Plato


class MenuRestaurant:
    @staticmethod
    def main():
        platosMenu = []
        while True:
            nombre = leer_texto("\nNombre del plato o bebida: ")
            precio = leer_decimal("Precio: $")
            es_bebida = confirmar("¿Es una bebida?")
            plato = Plato(nombre, precio, es_bebida)

            if not plato.esBebida:
                while True:
                    nombre_ingrediente = leer_texto("Ingrediente: ")
                    cantidad = leer_decimal("Cantidad: ", incluir_minimo=False)
                    unidad = leer_texto("Unidad de medida (gramos, unidades, etc.): ")
                    plato.agregar_ingrediente(Ingrediente(nombre_ingrediente, cantidad, unidad))
                    if not confirmar("¿Querés cargar otro ingrediente?"):
                        break

            plato.validar_ingredientes()
            platosMenu.append(plato)
            if not confirmar("¿Querés cargar otro plato o bebida?"):
                break

        print("\n----------- MENÚ -----------")
        for plato in platosMenu:
            print(f"{plato.nombreCompleto}\nPrecio: $ {plato.precio:.2f}")
            if not plato.esBebida:
                print(f"{'Ingredientes':<25} {'Cantidad':>10}  Unidad de medida")
                for ingrediente in plato.ingredientes:
                    print(f"{ingrediente.nombre:<25} {ingrediente.cantidad:>10g}  {ingrediente.unidadMedida}")
            print("----------------------------------")
