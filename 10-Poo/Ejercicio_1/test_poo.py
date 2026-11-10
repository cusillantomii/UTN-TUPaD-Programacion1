"""Pruebas de reglas de negocio y recorridos por el menú interactivo."""

from contextlib import redirect_stdout
from io import StringIO
import unittest
from unittest.mock import patch

from TP10_POO_CanelladaFacundo import main
from entrada import leer_decimal
from ejercicio_1_matriz.celda import Celda
from ejercicio_1_matriz.matriz import Matriz
from ejercicio_2_notas.alumno import Alumno
from ejercicio_2_notas.nota import Nota
from ejercicio_3_restaurante.ingrediente import Ingrediente
from ejercicio_3_restaurante.plato import Plato
from ejercicio_4_computadoras.componente_cpu import ComponenteCPU
from ejercicio_4_computadoras.computadora import Computadora
from ejercicio_5_barrio.barrio import Barrio
from ejercicio_5_barrio.habitacion import Habitacion
from ejercicio_5_barrio.vivienda import Vivienda


class PruebasPOO(unittest.TestCase):
    def test_matriz_rechaza_coordenada_duplicada_sin_reemplazar_valor(self):
        matriz = Matriz()
        matriz.agregar_celda(Celda(0, 0, "hola"))
        matriz.agregar_celda(Celda(0, 1, "otra"))
        with self.assertRaises(ValueError):
            matriz.agregar_celda(Celda(0, 0, "duplicada"))
        self.assertEqual(matriz.obtener_valor(0, 0), "hola")
        self.assertEqual(len(matriz.celdasMatriz), 2)
        self.assertEqual(matriz.obtener_valor(9, 9),
                         "La fila y columna indicada no ha sido asignada en ninguna celda")

    def test_listas_independientes_entre_instancias(self):
        primera = Matriz()
        segunda = Matriz()
        primera.agregar_celda(Celda(1, 1, "A"))
        self.assertEqual(segunda.celdasMatriz, [])
        ana = Alumno("Ana", 1)
        juan = Alumno("Juan", 2)
        ana.agregar_nota(Nota("Programación", 8))
        self.assertEqual(juan.notas, [])

    def test_promedio_y_al_menos_una_nota(self):
        alumno = Alumno("Ana", 1)
        with self.assertRaises(ValueError):
            alumno.calcular_promedio()
        alumno.agregar_nota(Nota("Programación", 8))
        alumno.agregar_nota(Nota("Matemática", 9.5))
        self.assertEqual(alumno.calcular_promedio(), 8.75)
