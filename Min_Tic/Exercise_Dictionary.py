# Definición de una función para leer datos de entrada
def leer_datos():
  
  # Lee una línea de entrada y la almacena como operación
  operacion = input()  

  # Lee una línea de entrada, la divide en palabras y la almacena como producto
  producto = input().split()  

  # Convierte el primer elemento de producto a entero
  producto[0] = int(producto[0])  

  # Convierte el tercer elemento de producto a flotante
  producto[2] = float(producto[2])  

  # Convierte el cuarto elemento de producto a entero
  producto[3] = int(producto[3])  

  # Devuelve la operación y la lista producto
  return operacion, producto  

# Definición de una función para actualizar datos en la base de datos
def actualiza(db, prod):

  # Si el primer elemento de producto está en las claves de la base de datos
  if prod[0] in db.keys():  

    # Actualiza los valores asociados a esa clave en la base de datos
    db[prod[0]] = prod[1:]  

    # Devuelve la base de datos actualizada y un indicador de actualización exitosa
    return db, True  

  # Devuelve la base de datos sin cambios y un indicador de actualización fallida
  return db, False  

# Definición de una función para calcular la media de los valores en la base de datos
def media(db):

  # Obtiene una lista de los valores en la base de datos
  valores = list(db.values())  

  # Inicializa una variable para el cálculo del promedio
  prom = 0  
  for i in range(len(valores)):

    # Suma el segundo valor de cada elemento a la variable prom
    prom += valores[i][1]  

  # Calcula el promedio dividiendo la suma total entre la cantidad de elementos
  prom /= len(valores)  

  # Devuelve el promedio calculado
  return prom  

# Creación de un diccionario con datos iniciales
dic = {
  1: ["Manzanas", 5000.0, 25],
  2: ['Limones', 2300.0, 15],
  # ... (otros elementos)
  10: ['Jamon', 15000.0, 10]
}

# Llamada a la función leer_datos() para obtener la operación y los datos del producto
op, prod = leer_datos()

# Comienza el bloque condicional para verificar la operación
if op == 'ACTUALIZAR':
  print('ACTUALIZAR')

  # Llama a la función actualiza() y actualiza la base de datos
  dic, bandera = actualiza(dic, prod)  
elif op == 'BORRAR':
  print('BORRAR')
  # ... (otros bloques condicionales para otras operaciones)
else:
  print("ERROR")

# Calcula el promedio de los valores en la base de datos utilizando la función media()
prom = media(dic)

# Verifica si hubo una actualización exitosa y muestra el resultado
if bandera:

  # Imprime el promedio redondeado a 1 decimal
  print(round(prom, 1))  
else:
  print("ERROR")
