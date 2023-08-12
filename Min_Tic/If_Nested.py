# Ejercicios condicionales 
sbase = float(input("Ingrese el salario base: "))
htrabajo = int(input("Ingrese las horas trabajadas: "))
vhora = sbase/160

if (htrabajo <= 40) and (htrabajo > 0):
  print("La persona gana solo el salario base. ")
  print(sbase)
elif (htrabajo > 40) and (htrabajo < 49):
  print("La persona realiza horas extra que se pagan al doble.")
  print(sbase + (htrabajo - 40)*2*vhora)
elif htrabajo >= 49:
  print("La persona realiza horas extra que se pagan al triple.")
  print((htrabajo - 48)*3*vhora + 2*8*vhora + sbase)
else:
  print("NA")
