#1-
print("Hola Mundo!")
#2-
nombre = input("Por favor, ingresa tu nombre: ")
print("Hola", nombre, "!")
#3-
nombre = input("Ingresa tu nombre: ")
apellido = input("Ingresa tu apellido: ")
edad = input("Ingresa tu edad: ")
pais = input("En que pais vives?: ")
print("Soy", nombre , apellido ,"tengo",
 edad , "anos y vivo en" , pais ,".")
#4-
radio = float(input("Ingresa el radio del circulo: "))
perimetro = 2*radio*3.14
area = (radio**2)*3.14
print("Para un circulo con radio:",radio)
print("El area es:",area)
print("El perimetro es:", perimetro)
#5-
segundos = float(input("Ingresa la cantidad de segundos: "))
horas = segundos / 3600
print(f"{segundos} segundos equivalen a, {horas:.2f} horas.")
#6-
numero = int(input("De que numero quieres ver la tabla de multiplicar?: "))
for i in range(1, 11):
    resultado = numero *i
    print(f"{numero} x {i} = {resultado}")
#7-
num1 = int(input("Ingresa el primer numero (distinto de 0): "))
num2 = int(input("Ingresa el segundo numero (distinto de 0): "))
suma = num1 + num2
resta = num1 - num2
multiplicacion = num1 * num2
division = num1 / num2
print(f" Resultados para {num1} y {num2} ")
print(f"Suma: {num1} + {num2} = {suma}")
print(f"Resta: {num1} - {num2} = {resta}")
print(f"Multiplicacion: {num1} * {num2} = {multiplicacion}")
print(f"Division: {num1} / {num2} = {division:.2f}")
#8-
peso = float(input("Ingresa tu peso en kg (ej: 75.5): "))
altura = float(input("Ingresa tu altura en metros (ej: 1.75): "))
imc = peso / altura** 2
print(f"Tu indice de Masa Corporal (IMC) es: {imc:.2f}")
#9-
celsius = float(input("Ingresa la temperatura en grados Celsius: "))
fahrenheit = (9 / 5) * celsius + 32
print(f"{celsius}C equivalen a {fahrenheit:.1f}")
#10-
num1 = float(input("Ingresa el primer numero: "))
num2 = float(input("Ingresa el segundo numero: "))
num3 = float(input("Ingresa el tercer numero: "))
suma_total = num1 + num2 + num3
promedio = suma_total / 3
print(f"El promedio de {num1}, {num2} y {num3} es: {promedio:.2f}")


