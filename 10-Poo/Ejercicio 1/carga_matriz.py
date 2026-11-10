from entrada import confirmar, leer_entero, leer_texto
from .celda import Celda
from .matriz import Matriz


def main():
    matriz = Matriz()
    print("\nCargá celdas. Las posiciones empiezan en 0; FIN termina la carga.")
    while True:
        valor = leer_texto("Valor de la celda (FIN para terminar): ")
        if valor.upper() == "FIN":
            break
        fila = leer_entero("Fila: ")
        columna = leer_entero("Columna: ")
        try:
            matriz.agregar_celda(Celda(fila, columna, valor))
        except ValueError as error:
            print(error)

    print("\nCELDAS CARGADAS")
    if not matriz.celdasMatriz:
        print("No se cargaron celdas.")
    for celda in matriz.celdasMatriz:
        print(celda)

    while confirmar("¿Querés consultar una posición?"):
        fila = leer_entero("Fila: ")
        columna = leer_entero("Columna: ")
        print(matriz.obtener_valor(fila, columna))
