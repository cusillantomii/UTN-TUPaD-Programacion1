from entrada import confirmar, leer_decimal, leer_entero, leer_texto
from .alumno import Alumno
from .nota import Nota


class CargaNotas:
    @staticmethod
    def main():
        alumnos = []
        while True:
            print("\nDATOS DEL ALUMNO")
            nombre = leer_texto("Nombre completo: ")
            legajo = leer_entero("Legajo: ", minimo=1)
            alumno = Alumno(nombre, legajo)

            # La pregunta se hace después de cargar: garantiza al menos una nota.
            while True:
                catedra = leer_texto("Cátedra: ")
                valor = leer_decimal("Nota del examen: ")
                alumno.agregar_nota(Nota(catedra, valor))
                if not confirmar("¿Querés cargar otra nota para este alumno?"):
                    break

            alumnos.append(alumno)
            if not confirmar("¿Querés cargar otro alumno?"):
                break

        print("\nALUMNOS Y NOTAS")
        for alumno in alumnos:
            print(alumno)
            for nota in alumno.notas:
                print(f"  {nota}")
            print(f"  Promedio: {alumno.calcular_promedio():.2f}")
