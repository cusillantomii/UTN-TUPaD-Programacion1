#Consigna 1
edad = int(input("¿cuantos años tenes? "))

if edad >=18:
    print("es mayor de edad")

else: 
    print("es menor de edad")

#Consigna 2
nota= int(input("ingrese la nota: "))
          
if nota >=6:
    print("Aprobado")

else:
    print("desaprobado")

#Consigna 3
numero = int(input("ingrese un numero: "))
if numero % 2 == 0:
    print("es numero par")
else:
    print("no es un numero par")

#Consigna 4
edad = int(input("ingrese su edad: "))

if edad < 12:
    print("eres un niño/a")
elif edad >= 12 and edad < 18:
    print("eres un adolescente")
elif edad >= 18 and edad < 30:
    print("eres un adulto/a joven")
else:
    print ("eres un adulto/a")

#Consigna 5
contraseña = input("ingrese una contraseña entre 8 y 14 digitos: ")
contraseña2 = len(contraseña)

if 8 <= contraseña2 <= 14:
    print("la contraseña ingresada es correcta")
else: 
    print("la contraseña es incorrecta, porfavor vuelve a intentarlo")

#Consigna 6
import random
from statistics import mode, median, mean

numeros_aleatorios = [random.randint(1, 100) for i in range(50)]
mi_media = mean (numeros_aleatorios)
mi_mediana = median (numeros_aleatorios)
mi_moda = mode (numeros_aleatorios)

print("Media:  ", mi_media)
print("Mediana: ", mi_mediana)
print("Moda:   ", mi_moda)

if mi_media > mi_mediana and mi_mediana > mi_moda:
    print("Sesgo positivo o a la derecha ")
elif mi_media < mi_mediana and mi_mediana < mi_moda:
    print("Sesgo negativo o a la izquierda ")
else:
    print("No tiene sesgo ")

#Consigna 7
oracion = input("escriba una frase o oracion: ")
vocales = ("a","e","i","o","u")

if oracion.endswith (vocales):
    print (oracion + "!")
else: 
    print(oracion)

#Consigna 8
nombre = input("ingrese su nombre: ")
print("opcion 1 (si quiere su nombre en MAYUSCULA)/ opcion 2 (si quiere su nombre en minuscula)/ opcion 3 (primer letra mayuscula)")
opciones = int(input("escriba una opciones (1, 2 o 3): "))

match opciones: 
    case 1:
     print(nombre.upper())
    
    case 2:
     print(nombre.lower())

    case 3: 
     print(nombre.title())

#Consigna 9
magnitud = float(input("Ingresá la magnitud del terremoto: "))

if magnitud < 3:
    print("Muy leve (imperceptible)")
elif magnitud >= 3 and magnitud < 4:
    print("Leve (ligeramente perceptible)")
elif magnitud >= 4 and magnitud < 5:
    print("Moderado (sentido por personas, generalmente no causa daños)")
elif magnitud >= 5 and magnitud < 6:
    print("Fuerte (puede causar daños en estructuras debiles)")
elif magnitud >= 6 and magnitud < 7:
    print("Muy Fuerte (puede causar daños significativos)")
else:
    print("Extremo (puede causar graves daños a gran escala)")

#Consigna 10
# Paso 1: Pedimos los datos
hemisferio = input("¿En que hemisferio estás? (N/S): ").upper()
mes = int(input("¿Que mes es? (1-12): "))
dia = int(input("¿Que día es? (1-31): "))

# Paso 2: Determinamos el periodo
if (mes == 12 and dia >= 21) or (mes <= 2) or (mes == 3 and dia <= 20):
    norte = "Invierno"
    sur   = "Verano"
elif (mes == 3 and dia >= 21) or (mes <= 5) or (mes == 6 and dia <= 20):
    norte = "Primavera"
    sur   = "Otoño"
elif (mes == 6 and dia >= 21) or (mes <= 8) or (mes == 9 and dia <= 20):
    norte = "Verano"
    sur   = "Invierno"
else:
    norte = "Otoño"
    sur   = "Primavera"

# Paso 3: Mostramos la estacion segun el hemisferio
if hemisferio == "N":
    print("Estás en:", norte)
elif hemisferio == "S":
    print("Estás en:", sur)
else:
    print("Hemisferio no válido. Ingresá N o S.")
     

