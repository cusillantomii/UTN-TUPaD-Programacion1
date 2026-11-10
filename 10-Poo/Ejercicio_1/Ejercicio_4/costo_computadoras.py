from entrada import confirmar, leer_decimal, leer_entero, leer_texto
from .componente_cpu import ComponenteCPU
from .computadora import Computadora


class CostoComputadora:
    @staticmethod
    def main():
        while True:
            marca = leer_texto("\nMarca de la computadora: ")
            modelo = leer_texto("Modelo: ")
            computadora = Computadora(marca, modelo)
            while True:
                nombre = leer_texto("Componente: ")
                marca_componente = leer_texto("Marca del componente: ")
                cantidad = leer_entero("Cantidad: ", minimo=1)
                precio = leer_decimal("Precio por unidad: $")
                componente = ComponenteCPU(nombre, marca_componente, cantidad, precio)
                computadora.agregar_componente(componente)
                if not confirmar("¿Querés cargar otro componente?"):
                    break

            print("\n----------- COMPUTADORA -----------")
            print(f"Marca: {computadora.marca}\nModelo: {computadora.modelo}")
            print(f"{'Componente':<24} {'Marca':<16} {'Cantidad':>8} {'Precio/unidad':>14} {'Subtotal':>12}")
            for componente in computadora.componentesCPU:
                print(f"{componente.componente:<24} {componente.marca:<16} "
                      f"{componente.cantidad:>8} {componente.precio:>14.2f} "
                      f"{componente.calcular_subtotal():>12.2f}")
            costo = computadora.calcular_costo()
            venta = computadora.calcular_precio_venta()
            print(f"Costo total: $ {costo:.2f}")
            print(f"Precio sugerido: {costo:.2f} + {venta - costo:.2f} = $ {venta:.2f}")
            if not confirmar("¿Querés cotizar una nueva computadora?"):
                break
