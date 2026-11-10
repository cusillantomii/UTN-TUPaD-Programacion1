class Plato:
    def __init__(self, nombreCompleto, precio, esBebida):
        self.nombreCompleto = nombreCompleto
        self.precio = precio
        self.esBebida = esBebida
        self.ingredientes = []

    def agregar_ingrediente(self, ingrediente):
        if self.esBebida:
            raise ValueError("Las bebidas se cargan sin ingredientes.")
        self.ingredientes.append(ingrediente)

    def validar_ingredientes(self):
        if not self.esBebida and not self.ingredientes:
            raise ValueError("Un plato que no es bebida debe tener al menos un ingrediente.")
