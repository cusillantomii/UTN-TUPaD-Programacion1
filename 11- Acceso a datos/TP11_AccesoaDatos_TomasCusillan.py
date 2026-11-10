"""Prueba integral solicitada: inicialización, altas, consulta, cambio y baja."""

from biblioteca.repositorio import RepositorioBiblioteca


def mostrar_libros(repositorio):
    libros = repositorio.listar_libros()
    if not libros:
        print("No hay libros registrados.")
    for libro in libros:
        print(libro)


def main():
    repositorio = RepositorioBiblioteca()
    repositorio.inicializar()
    print(f"Base SQLite: {repositorio.ruta_db}")

    # Usamos los IDs generados: no suponemos que sean 1, 2 o 3.
    id_borges = repositorio.registrar_autor("Jorge Luis Borges", "Argentina")
    id_allende = repositorio.registrar_autor("Isabel Allende", "Chile")
    id_ficciones = repositorio.registrar_libro("Ficciones", 1944, id_borges)
    repositorio.registrar_libro("El Aleph", 1949, id_borges)
    id_casa = repositorio.registrar_libro("La casa de los espíritus", 1982, id_allende)

    print("\n1. AUTORES REGISTRADOS")
    for autor in repositorio.obtener_autores_db():
        print(f"ID: {autor['id']} | {autor['nombre']} | {autor['nacionalidad']}")
    print("\n2. LIBROS REGISTRADOS (JOIN con autores)")
    mostrar_libros(repositorio)

    print("\n3. ACTUALIZACIÓN DE UN TÍTULO")
    repositorio.actualizar_titulo_libro(id_ficciones, "Ficciones - edición revisada")
    actualizado = repositorio.obtener_libro_db(id_ficciones)
    print(f"Verificación: {actualizado['titulo']}")

    print(f"\n4. ELIMINACIÓN DEL LIBRO CON ID {id_casa}")
    eliminado = repositorio.eliminar_libro(id_casa)
    print(f"Eliminación confirmada: {eliminado}")
    print("\n5. LISTADO FINAL")
    mostrar_libros(repositorio)


if __name__ == "__main__":
    main()
