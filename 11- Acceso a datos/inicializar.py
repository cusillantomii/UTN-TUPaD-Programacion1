"""Crea las tablas sin agregar datos de ejemplo ni borrar registros existentes."""

from biblioteca.repositorio import RepositorioBiblioteca


def main():
    repositorio = RepositorioBiblioteca()
    repositorio.inicializar()
    print(f"Base de datos lista: {repositorio.ruta_db}")


if __name__ == "__main__":
    main()
