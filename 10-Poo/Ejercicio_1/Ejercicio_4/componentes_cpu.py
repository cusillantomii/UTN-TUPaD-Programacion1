class ComponenteCPU:
    def __init__(self, componente, marca, cantidad, precio):
        self.componente = componente
        self.marca = marca
        self.cantidad = cantidad
        self.precio = precio

    def calcular_subtotal(self):
        return self.cantidad * self.precio
