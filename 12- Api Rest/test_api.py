"""Prueba HTTP con requests. Requiere que Flask esté en ejecución."""

import argparse

import requests


def comprobar_respuesta(respuesta, codigo_esperado):
    if respuesta.status_code != codigo_esperado:
        raise AssertionError(
            f"Se esperaba HTTP {codigo_esperado}; llegó {respuesta.status_code}: {respuesta.text}"
        )
    return respuesta.json()


def main(url_base="http://127.0.0.1:5000"):
    url_base = url_base.rstrip("/")
    with requests.Session() as cliente:
        # 1. Consultar el listado inicial.
        respuesta = cliente.get(f"{url_base}/api/libros", timeout=5)
        libros = comprobar_respuesta(respuesta, 200)
        print(f"1. GET libros: {len(libros)} libro(s).")

        # 2. Crear un autor y usar su ID para crear un libro.
        respuesta = cliente.post(
            f"{url_base}/api/autores",
            json={"nombre": "Autor de prueba API", "nacionalidad": "Argentina"},
            timeout=5,
        )
        autor = comprobar_respuesta(respuesta, 201)
        respuesta = cliente.post(
            f"{url_base}/api/libros",
            json={"titulo": "Libro de prueba API", "anio": 2026, "autor_id": autor["id"]},
            timeout=5,
        )
        libro = comprobar_respuesta(respuesta, 201)
        url_libro = f"{url_base}/api/libros/{libro['id']}"
        print(f"2. POST autor {autor['id']} y libro {libro['id']}: HTTP 201.")

        # 3. Actualizar únicamente el título y consultar para comprobar persistencia.
        respuesta = cliente.put(url_libro, json={"titulo": "Título actualizado desde requests"}, timeout=5)
        actualizado = comprobar_respuesta(respuesta, 200)
        if actualizado["titulo"] != "Título actualizado desde requests":
            raise AssertionError("La respuesta no contiene el título actualizado.")
        consultado = comprobar_respuesta(cliente.get(url_libro, timeout=5), 200)
        if consultado["titulo"] != actualizado["titulo"] or consultado["anio"] != libro["anio"]:
            raise AssertionError("El cambio no persistió o se modificó un campo no enviado.")
        print("3. PUT título y GET de verificación: HTTP 200.")

        # 4. Eliminar y verificar tanto el mensaje como la ausencia del registro.
        eliminado = comprobar_respuesta(cliente.delete(url_libro, timeout=5), 200)
        if eliminado.get("id") != libro["id"] or eliminado.get("mensaje") != "Libro eliminado correctamente.":
            raise AssertionError("La respuesta no confirma la eliminación del libro.")
        comprobar_respuesta(cliente.get(url_libro, timeout=5), 404)
        print("4. DELETE: HTTP 200. GET posterior: HTTP 404.")
    print("Prueba integral finalizada correctamente.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prueba HTTP del TP de API REST.")
    parser.add_argument("--url", default="http://127.0.0.1:5000", help="URL base del servidor Flask.")
    argumentos = parser.parse_args()
    try:
        main(argumentos.url)
    except (requests.RequestException, AssertionError, ValueError) as error:
        raise SystemExit(f"Falló la prueba: {error}")
