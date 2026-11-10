"""Pruebas de la API con SQLite temporal y una prueba HTTP real con requests."""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread
import unittest

from werkzeug.serving import make_server

from app import crear_app
from test_api import main as probar_con_requests


class PruebasAPI(unittest.TestCase):
    def setUp(self):
        self.temporal = TemporaryDirectory()
        self.addCleanup(self.temporal.cleanup)
        self.ruta = Path(self.temporal.name) / "biblioteca.db"
        self.app = crear_app(self.ruta)
        self.app.config["TESTING"] = True
        self.cliente = self.app.test_client()

    def crear_autor(self, nombre="Borges"):
        respuesta = self.cliente.post("/api/autores", json={"nombre": nombre, "nacionalidad": "Argentina"})
        self.assertEqual(respuesta.status_code, 201)
        return respuesta.get_json()

    def crear_libro(self):
        autor = self.crear_autor()
        respuesta = self.cliente.post("/api/libros", json={"titulo": "Ficciones", "anio": 1944, "autor_id": autor["id"]})
        self.assertEqual(respuesta.status_code, 201)
        return respuesta.get_json()

    def test_listados_vacios_devuelven_200(self):
        for ruta in ("/api/libros", "/api/autores"):
            respuesta = self.cliente.get(ruta)
            self.assertEqual(respuesta.status_code, 200)
            self.assertEqual(respuesta.get_json(), [])

    def test_crud_y_join_con_informacion_del_autor(self):
        libro = self.crear_libro()
        url = f"/api/libros/{libro['id']}"
        self.assertEqual(libro["autor"]["nombre"], "Borges")
        self.assertEqual(self.cliente.get("/api/libros").get_json()[0], libro)
        self.assertEqual(self.cliente.get(url).get_json(), libro)
        self.assertEqual(self.cliente.get(f"/api/autores/{libro['autor_id']}").status_code, 200)
        respuesta = self.cliente.put(url, json={"titulo": "Nuevo título"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.get_json()["titulo"], "Nuevo título")
        self.assertEqual(respuesta.get_json()["anio"], 1944)
        self.assertEqual(respuesta.get_json()["autor_id"], libro["autor_id"])
        otro_autor = self.crear_autor("Allende")
        respuesta = self.cliente.put(url, json={"anio": 1982, "autor_id": otro_autor["id"]})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.get_json()["autor"]["nombre"], "Allende")
        self.assertEqual(respuesta.get_json()["titulo"], "Nuevo título")
        self.assertEqual(self.cliente.delete(url).status_code, 200)
        self.assertEqual(self.cliente.get(url).status_code, 404)
        self.assertEqual(self.cliente.delete(url).status_code, 404)

    def test_ids_inexistentes_devuelven_404(self):
        self.assertEqual(self.cliente.get("/api/autores/999").status_code, 404)
        self.assertEqual(self.cliente.get("/api/libros/999").status_code, 404)
        self.assertEqual(self.cliente.put("/api/libros/999", json={"titulo": "Nuevo"}).status_code, 404)
        self.assertEqual(self.cliente.delete("/api/libros/999").status_code, 404)

    def test_campos_obligatorios(self):
        for ruta, datos in [
            ("/api/autores", {}),
            ("/api/autores", {"nombre": "Ana"}),
            ("/api/autores", {"nacionalidad": "Argentina"}),
            ("/api/libros", {"titulo": "Libro", "anio": 2026}),
            ("/api/libros", {"titulo": "Libro", "autor_id": 1}),
            ("/api/libros", {"anio": 2026, "autor_id": 1}),
        ]:
            with self.subTest(ruta=ruta, datos=datos):
                respuesta = self.cliente.post(ruta, json=datos)
                self.assertEqual(respuesta.status_code, 400)
                self.assertIn("error", respuesta.get_json())

    def test_tipos_valores_y_campos_desconocidos(self):
        autor = self.crear_autor()
        base = {"titulo": "Libro", "anio": 2026, "autor_id": autor["id"]}
        for campo, valor in [("titulo", " "), ("titulo", None), ("titulo", 123),
                             ("anio", "2026"), ("anio", True), ("anio", 2026.5), ("anio", 0),
                             ("autor_id", False), ("autor_id", -1), ("otro", "campo")]:
            with self.subTest(campo=campo, valor=valor):
                respuesta = self.cliente.post("/api/libros", json={**base, campo: valor})
                self.assertEqual(respuesta.status_code, 400)
        for datos in ({"nombre": " ", "nacionalidad": "AR"}, {"nombre": "Ana", "nacionalidad": None}):
            self.assertEqual(self.cliente.post("/api/autores", json=datos).status_code, 400)
        self.assertEqual(self.cliente.get("/api/libros").get_json(), [])

    def test_json_mal_formado_o_cuerpo_que_no_es_objeto(self):
        for cuerpo in ("{", "[]", "null", '"texto"', "123", "true"):
            with self.subTest(cuerpo=cuerpo):
                respuesta = self.cliente.post("/api/autores", data=cuerpo, content_type="application/json")
                self.assertEqual(respuesta.status_code, 400)
                self.assertIn("error", respuesta.get_json())
        self.assertEqual(self.cliente.post("/api/autores").status_code, 400)
        self.assertEqual(self.cliente.post("/api/autores", data="texto", content_type="text/plain").status_code, 400)

    def test_autor_inexistente_en_alta_y_actualizacion(self):
        datos = {"titulo": "Libro", "anio": 2026, "autor_id": 999}
        self.assertEqual(self.cliente.post("/api/libros", json=datos).status_code, 404)
        libro = self.crear_libro()
        url = f"/api/libros/{libro['id']}"
        self.assertEqual(self.cliente.put(url, json={"autor_id": 999}).status_code, 404)
        self.assertEqual(self.cliente.get(url).get_json(), libro)

    def test_put_invalido_no_modifica_el_libro(self):
        libro = self.crear_libro()
        url = f"/api/libros/{libro['id']}"
        for datos in ({}, {"titulo": None}, {"anio": True}, {"autor_id": 0}, {"campo_inexistente": "valor"}):
            with self.subTest(datos=datos):
                self.assertEqual(self.cliente.put(url, json=datos).status_code, 400)
                self.assertEqual(self.cliente.get(url).get_json(), libro)

    def test_errores_de_ruta_y_metodo_tambien_son_json(self):
        for respuesta, codigo in [(self.cliente.get("/ruta_inexistente"), 404),
                                   (self.cliente.delete("/api/autores"), 405)]:
            self.assertEqual(respuesta.status_code, codigo)
            self.assertIn("error", respuesta.get_json())

    def test_persistencia_al_recrear_la_aplicacion(self):
        libro = self.crear_libro()
        otra_app = crear_app(self.ruta)
        self.assertEqual(otra_app.test_client().get(f"/api/libros/{libro['id']}").get_json(), libro)

    def test_script_requests_con_servidor_http_real(self):
        servidor = make_server("127.0.0.1", 0, self.app)
        hilo = Thread(target=servidor.serve_forever, daemon=True)
        hilo.start()
        salida = StringIO()
        try:
            with redirect_stdout(salida):
                probar_con_requests(f"http://127.0.0.1:{servidor.server_port}")
        finally:
            servidor.shutdown()
            hilo.join(timeout=5)
            servidor.server_close()
        self.assertIn("Prueba integral finalizada correctamente.", salida.getvalue())
        self.assertEqual(self.cliente.get("/api/libros").get_json(), [])


if __name__ == "__main__":
    unittest.main()
