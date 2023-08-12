# 1. Abrir el archivo:
archivo = open('/content/vtainternet.txt', 'r')
# 2. Leer el archivo:
lista = []
for linea in archivo:
  if linea[-1] == '\n':
    lista.append(int(linea[:-1]))
  else:
    lista.append(int(linea))
print(lista)
# 3. Cerrar el archivo:
archivo.close()
