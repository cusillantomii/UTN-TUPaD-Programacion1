class Barrio:
    def __init__(self, nombre, empresaConstructora):
        self.nombre = nombre
        self.empresaConstructora = empresaConstructora
        self.viviendas = []

    def agregar_vivienda(self, vivienda):
        self.viviendas.append(vivienda)

    def getSuperficieTotalTerreno(self):
        total = 0
        for vivienda in self.viviendas:
            total += vivienda.superficieTerreno
        return total

    def getSuperficieTotalTerrenoXManzana(self, manzana):
        total = 0
        for vivienda in self.viviendas:
            if vivienda.manzana == manzana:
                total += vivienda.superficieTerreno
        return total

    def getSuperficieTotalCubierta(self):
        total = 0
        for vivienda in self.viviendas:
            # Reutilizamos la validación de cada vivienda, como pide la consigna.
            total += vivienda.getMetrosCuadradosCubiertos()
        return total
