"""Funciones de entrada compartidas por los cinco ejercicios del TP."""

from math import isfinite


def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("El texto no puede quedar vacío.")


def leer_entero(mensaje, minimo=0):
    while True:
        try:
            numero = int(input(mensaje))
            if numero >= minimo:
                return numero
        except ValueError:
            pass
        print(f"Ingresá un número entero mayor o igual a {minimo}.")


def leer_decimal(mensaje, minimo=0, incluir_minimo=True):
    while True:
        try:
            numero = float(input(mensaje).replace(",", "."))
            cumple_minimo = numero >= minimo if incluir_minimo else numero > minimo
            if isfinite(numero) and cumple_minimo:
                return numero
        except ValueError:
            pass
        relacion = "mayor o igual a" if incluir_minimo else "mayor a"
        print(f"Ingresá un número decimal finito {relacion} {minimo}.")


def confirmar(mensaje):
    while True:
        respuesta = input(f"{mensaje} (SI/NO): ").strip().upper()
        if respuesta in ("SI", "SÍ", "S"):
            return True
        if respuesta in ("NO", "N"):
            return False
        print("Respondé SI o NO.")
