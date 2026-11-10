class Habitacion:
    def __init__(self, nombre, metrosCuadrados):
        if metrosCuadrados <= 0:
            raise ValueError("Los metros cuadrados de la habitación deben ser positivos.")
        self.nombre = nombre
        self.metrosCuadrados = metrosCuadrados
