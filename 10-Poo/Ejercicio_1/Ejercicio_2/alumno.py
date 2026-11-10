class Alumno:
    def __init__(self, nombreCompleto, legajo):
        self.nombreCompleto = nombreCompleto
        self.legajo = legajo
        self.notas = []

    def agregar_nota(self, nota):
        self.notas.append(nota)

    def calcular_promedio(self):
        if not self.notas:
            raise ValueError("El alumno debe tener al menos una nota.")
        total = 0
        for nota in self.notas:
            total += nota.notaExamen
        return total / len(self.notas)

    def __str__(self):
        return f"{self.nombreCompleto} | Legajo: {self.legajo}"
