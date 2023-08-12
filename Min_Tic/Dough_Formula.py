//Calcular la masa, la cual consiste en masa = presión * volumen / a.37 * (temperatura+460)
presion = float(input("Ingrese el valor de la presión: "))
volumen = float(input("Ingrese el volumen: "))
temperatura = float(input("Ingrese la temperatura: "))

masa = (presion*volumen)/(0.37*(temperatura+460))

print("El valor de la masa de aire es: ",round(masa,2))

