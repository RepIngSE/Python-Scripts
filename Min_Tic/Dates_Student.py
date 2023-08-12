#Ingresar los nombres del estudiante.
nombre_estudiante = input("Ingrese el nombre del estudiante\n")

#Ingresar la ID del estudiante.
id_estudiante = input("Ingrese la identificaciòn del estudiante:\n")

#Ingresar notas de primer corte y talleres correspondientes 
notaTaller1 = float(input("Ingrese nota del taller 1:\n"))
notaTaller2 = float(input("Ingrese nota del taller 2:\n"))
notaTaller3 = float(input("Ingrese nota del taller 3:\n"))

#Obtener el ponderado de primer corte
nota_corte1 = ((notaTaller1 + notaTaller2 + notaTaller3) / 3) * 0.3

#Leer nota de evaluaciones de segundo corte
notaEvaluacion1, notaEvaluacion2 = input("Ingrese la nota de la evaluación 1 y 2 separadas:").split()

#Ingrese la nota de la evaluación 1 y 2 separadas
notaEvaluacion1 = float(notaEvaluacion1)
notaEvaluacion2 = float(notaEvaluacion2)

#Hallar el valor ponderado del corte 2
nota_corte2 = ((notaEvaluacion1 + notaEvaluacion2) / 2) * 0.3

#Leer las notas de trabajo y sustentación
notatrabajo = float(input("Ingrese nota trabajo:\n"))

notasustentacion = float(input("Ingrese nota sustentación:\n"))

#Obtener ponderado de nota corte 3 (40%)
nota_corte3 = (notatrabajo*0.5 + notasustentacion*0.5)*0.4

#Obtener nota definitiva
nota_definitiva = nota_corte1 + nota_corte2 + nota_corte3
print("La nota definitiva es: ", round(nota_definitiva, 1))
