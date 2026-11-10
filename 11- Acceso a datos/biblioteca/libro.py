class Libro:
    def __init__(self, id_libro, titulo, anio_publicacion, autor):
        self.id_libro = id_libro
        self.titulo = titulo
        self.anio_publicacion = anio_publicacion
        # Agregación: recibimos un Autor que ya existe.
        self.autor = autor

    def __str__(self):
        return (f"ID: {self.id_libro} | {self.titulo} ({self.anio_publicacion}) "
                f"| Autor: {self.autor.nombre}")
