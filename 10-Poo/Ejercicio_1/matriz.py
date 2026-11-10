class Matriz:
    def __init__(self):
        # Dentro de __init__: cada matriz tiene su propia lista.
        self.celdasMatriz = []

    def buscar_celda(self, fila, columna):
        for celda in self.celdasMatriz:
            if celda.fila == fila and celda.columna == columna:
                return celda
        return None

    def agregar_celda(self, celda):
        if self.buscar_celda(celda.fila, celda.columna) is not None:
            raise ValueError("Ya existe una celda en esa fila y columna.")
        self.celdasMatriz.append(celda)

    def obtener_valor(self, fila, columna):
        celda = self.buscar_celda(fila, columna)
        if celda is None:
            return "La fila y columna indicada no ha sido asignada en ninguna celda"
        return celda.valor
