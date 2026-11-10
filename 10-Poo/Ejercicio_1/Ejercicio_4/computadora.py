class Computadora:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo
        self.componentesCPU = []

    def agregar_componente(self, componente):
        self.componentesCPU.append(componente)

    def calcular_costo(self):
        total = 0
        for componente in self.componentesCPU:
            total += componente.calcular_subtotal()
        return total

    def calcular_precio_venta(self):
        costo = self.calcular_costo()
        # El enunciado omite el caso de igualdad: adoptamos 30% desde $50.000.
        if costo < 50000:
            recargo = 0.40
        else:
            recargo = 0.30
        return costo + costo * recargo
