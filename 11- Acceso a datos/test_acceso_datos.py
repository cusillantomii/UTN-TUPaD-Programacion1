from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from TP11_AccesoADatos_CanelladaFacundo import main as ejecutar_demostracion
from biblioteca.autor import Autor
from biblioteca.libro import Libro
from biblioteca.repositorio import RepositorioBiblioteca


class PruebasAccesoDatos(unittest.TestCase):
    def setUp(self):
        self.temporal = TemporaryDirectory()
        self.addCleanup(self.temporal.cleanup)
        self.ruta = Path(self.temporal.name) / "biblioteca.db"
        self.repositorio = RepositorioBiblioteca(self.ruta)
        self.repositorio.inicializar()

    def test_modelos_y_agregacion(self):
        autor = Autor(1, "Borges", "Argentina")
        libro = Libro(2, "Ficciones", 1944, autor)
        self.assertIs(libro.autor, autor)
        self.assertIn("Borges", str(autor))
        self.assertIn("Ficciones", str(libro))

    def test_programa_principal_completo_sobre_base_temporal(self):
        salida = StringIO()
        with patch("TP11_AccesoADatos_CanelladaFacundo.RepositorioBiblioteca", return_value=self.repositorio):
            with redirect_stdout(salida):
                ejecutar_demostracion()
        self.assertEqual(len(self.repositorio.obtener_autores_db()), 2)
        self.assertEqual(len(self.repositorio.listar_libros()), 2)
        self.assertIn("Ficciones - edición revisada", salida.getvalue())
        self.assertIn("Eliminación confirmada: True", salida.getvalue())

    def test_secuencia_integral_y_persistencia_entre_conexiones(self):
        id_uno = self.repositorio.registrar_autor("Borges", "Argentina")
        id_dos = self.repositorio.registrar_autor("Allende", "Chile")
        primero = self.repositorio.registrar_libro("Ficciones", 1944, id_uno)
        self.repositorio.registrar_libro("El Aleph", 1949, id_uno)
        ultimo = self.repositorio.registrar_libro("La casa de los espíritus", 1982, id_dos)
        libros = self.repositorio.listar_libros()
        self.assertEqual(len(libros), 3)
        self.assertEqual(libros[0].autor.nombre, "Borges")
        self.assertTrue(self.repositorio.actualizar_titulo_libro(primero, "Ficciones revisadas"))
        self.assertTrue(self.repositorio.eliminar_libro(ultimo))
        otro_repositorio = RepositorioBiblioteca(self.ruta)
        otro_repositorio.inicializar()  # No borra datos existentes.
        self.assertEqual(len(otro_repositorio.listar_libros()), 2)
        self.assertEqual(otro_repositorio.obtener_libro_db(primero)["titulo"], "Ficciones revisadas")

    def test_clave_foranea_rechaza_autor_inexistente(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.repositorio.registrar_libro("Sin autor", 2026, 999)
        self.assertEqual(self.repositorio.obtener_libros_db(), [])

    def test_consultas_parametrizadas_preservan_texto_y_tablas(self):
        id_autor = self.repositorio.registrar_autor("O'Connor", "Irlanda")
        titulo = "Libro'); DROP TABLE autores; --"
        id_libro = self.repositorio.registrar_libro(titulo, 2026, id_autor)
        self.assertEqual(self.repositorio.obtener_libro_db(id_libro)["titulo"], titulo)
        self.assertEqual(self.repositorio.obtener_autor_db(id_autor)["nombre"], "O'Connor")

    def test_actualizacion_completa_y_registros_inexistentes(self):
        autor = self.repositorio.insertar_autor_db("Ana", "Argentina")
        otro = self.repositorio.insertar_autor_db("Juan", "Uruguay")
        libro = self.repositorio.insertar_libro_db("Antes", 2000, autor["id"])
        self.assertTrue(self.repositorio.actualizar_libro_db(libro["id"], "Después", 2001, otro["id"]))
        actualizado = self.repositorio.obtener_libro_db(libro["id"])
        self.assertEqual(actualizado["autor"]["nombre"], "Juan")
        self.assertEqual(actualizado["anio"], 2001)
        self.assertIsNone(self.repositorio.obtener_autor_db(999))
        self.assertIsNone(self.repositorio.obtener_libro_db(999))
        self.assertFalse(self.repositorio.actualizar_titulo_libro(999, "Inexistente"))
        self.assertFalse(self.repositorio.actualizar_libro_db(999, "Inexistente", 2001, autor["id"]))
        self.assertFalse(self.repositorio.eliminar_libro_db(999))


if __name__ == "__main__":
    unittest.main()
