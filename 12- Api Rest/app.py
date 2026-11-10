"""TP 12: API REST de biblioteca. Ejecutar este archivo inicia Flask."""

import sqlite3

from flask import Flask, jsonify, request

from repositorio_api import RepositorioBiblioteca


def leer_json(campos_permitidos):
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict) or not datos:
        raise ValueError("Enviá un objeto JSON no vacío con los campos solicitados.")
    desconocidos = set(datos) - set(campos_permitidos)
    if desconocidos:
        raise ValueError(f"Campos desconocidos: {', '.join(sorted(desconocidos))}.")
    return datos


def validar_texto(datos, campo):
    valor = datos.get(campo)
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"El campo '{campo}' es obligatorio y debe ser un texto no vacío.")
    return valor.strip()


def validar_entero_positivo(datos, campo):
    valor = datos.get(campo)
    # En Python bool hereda de int: comprobamos el tipo exacto para rechazar true.
    if type(valor) is not int or valor <= 0:
        raise ValueError(f"El campo '{campo}' es obligatorio y debe ser un entero positivo.")
    return valor


def crear_app(ruta_db=None):
    app = Flask(__name__)
    app.json.ensure_ascii = False
    repositorio = RepositorioBiblioteca() if ruta_db is None else RepositorioBiblioteca(ruta_db)
    repositorio.inicializar()

    @app.errorhandler(ValueError)
    def datos_invalidos(error):
        return jsonify({"error": str(error)}), 400

    @app.errorhandler(sqlite3.IntegrityError)
    def integridad_invalida(error):
        return jsonify({"error": "Los datos no respetan las restricciones de la biblioteca."}), 400

    @app.errorhandler(404)
    def ruta_inexistente(error):
        return jsonify({"error": "La ruta solicitada no existe."}), 404

    @app.errorhandler(405)
    def metodo_no_permitido(error):
        return jsonify({"error": "Ese método HTTP no está permitido para esta ruta."}), 405

    # Recursos de autores.
    @app.route("/api/autores", methods=["GET"])
    def obtener_autores():
        return jsonify(repositorio.obtener_autores_db()), 200

    @app.route("/api/autores/<int:id_autor>", methods=["GET"])
    def obtener_autor(id_autor):
        autor = repositorio.obtener_autor_db(id_autor)
        if autor is None:
            return jsonify({"error": "Autor no encontrado."}), 404
        return jsonify(autor), 200

    @app.route("/api/autores", methods=["POST"])
    def crear_autor():
        datos = leer_json(("nombre", "nacionalidad"))
        nombre = validar_texto(datos, "nombre")
        nacionalidad = validar_texto(datos, "nacionalidad")
        autor = repositorio.insertar_autor_db(nombre, nacionalidad)
        return jsonify(autor), 201

    # Recursos de libros.
    @app.route("/api/libros", methods=["GET"])
    def obtener_libros():
        return jsonify(repositorio.obtener_libros_db()), 200

    @app.route("/api/libros/<int:id_libro>", methods=["GET"])
    def obtener_libro(id_libro):
        libro = repositorio.obtener_libro_db(id_libro)
        if libro is None:
            return jsonify({"error": "Libro no encontrado."}), 404
        return jsonify(libro), 200

    @app.route("/api/libros", methods=["POST"])
    def crear_libro():
        datos = leer_json(("titulo", "anio", "autor_id"))
        titulo = validar_texto(datos, "titulo")
        anio = validar_entero_positivo(datos, "anio")
        autor_id = validar_entero_positivo(datos, "autor_id")
        if repositorio.obtener_autor_db(autor_id) is None:
            return jsonify({"error": "Autor no encontrado. Registralo antes de cargar el libro."}), 404
        libro = repositorio.insertar_libro_db(titulo, anio, autor_id)
        return jsonify(libro), 201

    @app.route("/api/libros/<int:id_libro>", methods=["PUT"])
    def actualizar_libro(id_libro):
        libro = repositorio.obtener_libro_db(id_libro)
        if libro is None:
            return jsonify({"error": "Libro no encontrado."}), 404

        datos = leer_json(("titulo", "anio", "autor_id"))
        # El TP pide enviar los campos a modificar: conservamos los demás.
        nuevos_datos = {
            "titulo": datos.get("titulo", libro["titulo"]),
            "anio": datos.get("anio", libro["anio"]),
            "autor_id": datos.get("autor_id", libro["autor_id"]),
        }
        titulo = validar_texto(nuevos_datos, "titulo")
        anio = validar_entero_positivo(nuevos_datos, "anio")
        autor_id = validar_entero_positivo(nuevos_datos, "autor_id")
        if repositorio.obtener_autor_db(autor_id) is None:
            return jsonify({"error": "Autor no encontrado."}), 404
        if not repositorio.actualizar_libro_db(id_libro, titulo, anio, autor_id):
            return jsonify({"error": "Libro no encontrado."}), 404
        return jsonify(repositorio.obtener_libro_db(id_libro)), 200

    @app.route("/api/libros/<int:id_libro>", methods=["DELETE"])
    def eliminar_libro(id_libro):
        if not repositorio.eliminar_libro_db(id_libro):
            return jsonify({"error": "Libro no encontrado."}), 404
        return jsonify({"mensaje": "Libro eliminado correctamente.", "id": id_libro}), 200

    return app


app = crear_app()


def main():
    app.run(host="127.0.0.1", port=5000, debug=False)


if __name__ == "__main__":
    main()
