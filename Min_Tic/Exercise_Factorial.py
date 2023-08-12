# factorial:
def factorial(n):
  if n <= 1:
    return 1
  else:
    return n * factorial(n-1)

X = int(input("Ingrese el valor a obtener su factorial: "))
factorial(X)
