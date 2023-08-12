# Definición de una función para leer datos de entrada
def leer_datos():

    # Lee dos valores enteros separados por espacio para n y k
    n, k = [int(x) for x in list(input().split(' '))]  

    # Lee una lista de números enteros para baldosa
    baldosa = [int(x) for x in list(input().split(' '))]  

    # Devuelve los valores leídos
    return n, k, baldosa  

# Llama a la función leer_datos(), pero el resultado no se almacena o utiliza en este punto
leer_datos()

# Definición de otra función para leer datos de entrada
def leer_datos_2():

    # Lee una lista de valores en una sola línea
    x = list(input().split())  

    # Extrae n y k de la lista
    n, k = int(x[0]), int(x[1])  

    # Lee otra lista de valores
    x = list(input().split())  
    baldosa = []
    for item in x:

        # Convierte y agrega cada elemento a la lista baldosa
        baldosa.append(int(item))  

    # Devuelve los valores leídos
    return n, k, baldosa  

# Llama a la función leer_datos_2(), pero el resultado no se almacena o utiliza en este punto
leer_datos_2()

# Lee una lista de valores en una sola línea
x = input().split()  

# Imprime la lista y su tipo
print(x, type(x))  

# Definición de una función para verificar fallas en la lista de baldosas
def verificar_fallas(baldosa, k):
    fallas_totales = 0
    falla_detectada = 0

    # Crea un diccionario vacío
    diccionario = {}  
    
    # Recorre la lista de baldosas junto con su índice
    for count, value in enumerate(baldosa):
        if (value in diccionario and count - diccionario.get(value) <= k):
          
            # Incrementa el contador de fallas detectadas
            falla_detectada += 1  
        if (value in diccionario):

            # Incrementa el contador de fallas totales
            fallas_totales += 1  

        # Almacena el índice actual en el diccionario
        diccionario[value] = count  

    # Devuelve los contadores de fallas
    return fallas_totales, falla_detectada  

# Llamada a la función leer_datos() para obtener n, k y baldosa
n, k, baldosa = leer_datos()

# Llamada a la función verificar_fallas() para obtener los resultados, pero el resultado no se almacena o utiliza en este punto
verificar_fallas(baldosa, k)

# Llamada a la función leer_datos() nuevamente para obtener n, k y baldosa
n, k, baldosa = leer_datos()

# Llamada a la función verificar_fallas() para obtener los resultados y se almacenan en fallas_totales y falla_detectada
fallas_totales, falla_detectada = verificar_fallas(baldosa, k)

# Imprime los resultados obtenidos de verificar_fallas y la longitud de la lista baldosa
print(fallas_totales, falla_detectada, len(baldosa))

# Creación de una lista que contiene varios tipos de elementos
lista = ['H', 'O', 'L', 'A', 12, False, (1, 2)]

# Recorre la lista junto con su índice e imprime cada elemento y su índice
for count, value in enumerate(lista):
    print(count, value)

# Creación de un diccionario vacío
diccionario = dict()
print(diccionario)

# Creación de un diccionario con elementos
dic_1 = {1: 'H', 3: 'O'}
value = 'H'

# Verifica si value está en el diccionario dic_1 e imprime un mensaje
if value in dic_1:
    print('El valor es:', value)
else:
    print('No está')

# Creación de una lista y un diccionario con elementos
lista = [1, 2, 3, 4, 5]
dic_2 = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4}
print(dic_2)

# Asignación de valores y manipulación de un diccionario
value = 1
count = 0
k = 1
falla_detectada = 0

dic_2['Hola'] = 5  # Agrega un elemento al diccionario
print(dic_2)

# Recorrido de una cadena usando enumerate y muestra su posición y valor
vec = 'Hola'
for pos, valor in enumerate(vec):
    print(pos, valor)

# Acceso a un elemento específico en una lista
vec = [1.2, 2.3, 3.4, 4.5]
print(vec[2])

# Creación de un diccionario vacío utilizando la función dict()
NewD = {}
# Muestra el tipo de NewD
print(type(NewD))

# Creación de un diccionario utilizando la función dict() y muestra su tipo
f = dict()
print(type(f))

# Creación de una lista de baldosas y variables para el cálculo de fallas
baldosa = ['H', 'O', 'L', 'H', 'O']
k = 3
fallas_totales = 0
falla_detectada = 0
diccionario = {}

# Recorrido de la lista de baldosas y cálculo de fallas utilizando un diccionario
for count, value in enumerate(baldosa):
    if (value in diccionario and count - diccionario.get(value) <= k):
        falla_detectada += 1

        # Imprime un mensaje en caso de detectar una falla
        print('Bandera', count)  
    if (value in diccionario):
        fallas_totales += 1

        # Imprime un mensaje en caso de encontrar una falla
        print('Bandera2', count)  
    diccionario[value] = count

    # Imprime el diccionario después de cada iteración
    print(diccionario)  

# Imprime los resultados finales de las fallas detectadas y totales
print(fallas_totales, falla_detectada)
