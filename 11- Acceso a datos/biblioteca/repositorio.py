"""Persistencia SQLite compartida por los TP 11 y 12.

Los métodos del TP 11 devuelven IDs, objetos o booleanos. Los terminados en
_db preparan los diccionarios que el TP 12 convierte a JSON.
"""

from contextlib import closing
from pathlib import Path
import sqlite3

from .autor import Autor
from .libro import Libro


RUTA_DB = Path(__file__).resolve().parent.parent / "biblioteca.db"

CONSULTA_LIBROS = """
    SELECT libros.id, libros.titulo, libros.anio, libros.autor_id,
           autores.nombre AS autor_nombre,
           autores.nacionalidad AS autor_nacionalidad
    FROM libros
    JOIN autores ON libros.autor_id = autores.id
"""


def libro_a_diccionario(fila):
    return {
        "id": fila["id"],
        "titulo": fila["titulo"],
        "anio": fila["anio"],
        "autor_id": fila["autor_id"],
        "autor": {
            "id": fila["autor_id"],
            "nombre": fila["autor_nombre"],
            "nacionalidad": fila["autor_nacionalidad"],
        },
    }


class RepositorioBiblioteca:
    def __init__(self, ruta_db=RUTA_DB):
        self.ruta_db = Path(ruta_db)

    def conectar(self):
        conexion = sqlite3.connect(self.ruta_db)
        conexion.row_factory = sqlite3.Row  # Permite leer fila["titulo"].
        conexion.execute("PRAGMA foreign_keys = ON")
        return conexion

    def inicializar(self):
        # closing cierra la conexión incluso si una operación lanza una excepción.
        with closing(self.conectar()) as conexion:
            conexion.executescript("""
                CREATE TABLE IF NOT EXISTS autores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    nacionalidad TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS libros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    anio INTEGER NOT NULL,
                    autor_id INTEGER NOT NULL,
                    FOREIGN KEY (autor_id) REFERENCES autores(id)
                );
            """)
            conexion.commit()

    # Ejercicio 3 del TP 11: operaciones CRUD.
    def registrar_autor(self, nombre, nacionalidad):
        with closing(self.conectar()) as conexion:
            cursor = conexion.execute(
                "INSERT INTO autores (nombre, nacionalidad) VALUES (?, ?)",
                (nombre, nacionalidad),
            )
            conexion.commit()
            return cursor.lastrowid

    def registrar_libro(self, titulo, anio, autor_id):
        with closing(self.conectar()) as conexion:
            cursor = conexion.execute(
                "INSERT INTO libros (titulo, anio, autor_id) VALUES (?, ?, ?)",
                (titulo, anio, autor_id),
            )
            conexion.commit()
            return cursor.lastrowid

    def listar_libros(self):
        libros = []
        for datos in self.obtener_libros_db():
            datos_autor = datos["autor"]
            autor = Autor(datos_autor["id"], datos_autor["nombre"], datos_autor["nacionalidad"])
            libro = Libro(datos["id"], datos["titulo"], datos["anio"], autor)
            libros.append(libro)
        return libros

    def actualizar_titulo_libro(self, id_libro, nuevo_titulo):
        with closing(self.conectar()) as conexion:
            cursor = conexion.execute(
                "UPDATE libros SET titulo = ? WHERE id = ?", (nuevo_titulo, id_libro)
            )
            conexion.commit()
            return cursor.rowcount > 0

    def eliminar_libro(self, id_libro):
        with closing(self.conectar()) as conexion:
            cursor = conexion.execute("DELETE FROM libros WHERE id = ?", (id_libro,))
            conexion.commit()
            return cursor.rowcount > 0

    # Ejercicio 1 del TP 12: métodos que utilizarán las rutas Flask.
    def obtener_autores_db(self):
        with closing(self.conectar()) as conexion:
            filas = conexion.execute("SELECT id, nombre, nacionalidad FROM autores ORDER BY id").fetchall()
            return [dict(fila) for fila in filas]

    def obtener_autor_db(self, id_autor):
        with closing(self.conectar()) as conexion:
            fila = conexion.execute(
                "SELECT id, nombre, nacionalidad FROM autores WHERE id = ?", (id_autor,)
            ).fetchone()
            return dict(fila) if fila is not None else None

    def insertar_autor_db(self, nombre, nacionalidad):
        id_autor = self.registrar_autor(nombre, nacionalidad)
        return self.obtener_autor_db(id_autor)

    def obtener_libros_db(self):
        with closing(self.conectar()) as conexion:
            filas = conexion.execute(CONSULTA_LIBROS + " ORDER BY libros.id").fetchall()
            return [libro_a_diccionario(fila) for fila in filas]

    def obtener_libro_db(self, id_libro):
        with closing(self.conectar()) as conexion:
            fila = conexion.execute(
                CONSULTA_LIBROS + " WHERE libros.id = ?", (id_libro,)
            ).fetchone()
            return libro_a_diccionario(fila) if fila is not None else None

    def insertar_libro_db(self, titulo, anio, autor_id):
        id_libro = self.registrar_libro(titulo, anio, autor_id)
        return self.obtener_libro_db(id_libro)

    def actualizar_libro_db(self, id_libro, titulo, anio, autor_id):
        with closing(self.conectar()) as conexion:
            cursor = conexion.execute(
                "UPDATE libros SET titulo = ?, anio = ?, autor_id = ? WHERE id = ?",
                (titulo, anio, autor_id, id_libro),
            )
            conexion.commit()
            return cursor.rowcount > 0

    def eliminar_libro_db(self, id_libro):
        return self.eliminar_libro(id_libro)
