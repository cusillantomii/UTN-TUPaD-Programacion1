#ESTRUCTURAS REPETITIVAS

#Ejercicio 1:
for i in range(101):
    print(i)

#Ejercicio 2:
numero = int(input("Ingrese un número entero: "))
numero = abs(numero)  # por si ingresan un número negativo
cantidad_digitos = len(str(numero))
print(f"El número tiene {cantidad_digitos} dígitos.")

#Ejercicio 3:
valor1 = int(input("Ingrese el primer valor: "))
valor2 = int(input("Ingrese el segundo valor: "))

inicio = min(valor1, valor2) + 1
fin = max(valor1, valor2)

suma = 0
for numero in range(inicio, fin):
    suma += numero

print(f"La suma de los números entre {valor1} y {valor2} (sin incluirlos) es: {suma}")

#Ejercicio 4:
total = 0
while True:
    numero = int(input("Ingrese un número (0 para terminar): "))
    if numero == 0:
        break
    total += numero

print(f"El total acumulado es: {total}")

# Ejercicio 5:
import random

numero_secreto = random.randint(0, 9)
intentos = 0
adivino = False

while not adivino:
    intento = int(input("Adivina el número (entre 0 y 9): "))
    intentos += 1
    if intento == numero_secreto:
        adivino = True
        print(f"¡Correcto! Adivinaste el número en {intentos} intento(s).")
    else:
        print("Incorrecto, intenta de nuevo.")

#Ejercicio 6:
for i in range(100, -1, -2):
    print(i)

#Ejericicio 7:
numero = int(input("Ingrese un número entero positivo: "))

suma = 0
for i in range(numero + 1):
    suma += i

print(f"La suma de 0 a {numero} es: {suma}")

#Ejercicio 8:
CANTIDAD_NUMEROS = 100  # cambiando solo este valor se ajusta la cantidad a procesar

pares = 0
impares = 0
negativos = 0
positivos = 0

for i in range(CANTIDAD_NUMEROS):
    numero = int(input(f"Ingrese el número {i + 1}: "))
    
    if numero % 2 == 0:
        pares += 1
    else:
        impares += 1
    
    if numero < 0:
        negativos += 1
    elif numero > 0:
        positivos += 1

print(f"Cantidad de números pares: {pares}")
print(f"Cantidad de números impares: {impares}")
print(f"Cantidad de números negativos: {negativos}")
print(f"Cantidad de números positivos: {positivos}")

#Ejercicio 9:
CANTIDAD_NUMEROS = 100  # cambiando solo este valor se ajusta la cantidad a procesar

suma = 0

for i in range(CANTIDAD_NUMEROS):
    numero = int(input(f"Ingrese el número {i + 1}: "))
    suma += numero

media = suma / CANTIDAD_NUMEROS
print(f"La media de los {CANTIDAD_NUMEROS} números es: {media}")

#Ejercicio 10:
numero = int(input("Ingrese un número entero: "))

numero_invertido = 0
numero_original = numero
numero = abs(numero)  # por si ingresan un número negativo

while numero > 0:
    digito = numero % 10
    numero_invertido = numero_invertido * 10 + digito
    numero = numero // 10

if numero_original < 0:
    numero_invertido = -numero_invertido

print(f"El número invertido es: {numero_invertido}")