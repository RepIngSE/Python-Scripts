#Import any library in this cell
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl

#Please Load the Dataframe here

#Cargar dataframe 
print("Carga del Dataframe")
url = 'https://raw.githubusercontent.com/Shiroyasha95/ICXRawData/main/Info%20intervals%202021-2023(1).csv'
df = pd.read_csv(url)

#Sacar promedio de llamadas por año dependiendo de la in formación suministrada 
df['Date'] = pd.to_datetime(df['Date'])
df['Año'] = df['Date'].dt.year 

print("Promedio por año del campo IB Calls\n")
df_promedio1 = df.groupby('Año')['IB Calls'].mean().reset_index()
print(df_promedio1,"\n")

print("Promedio por año del campo IB Handled\n")
df_promedio2 = df.groupby('Año')['IB Handled'].mean().reset_index()
print(df_promedio2,"\n")

#Sacar promedio de llamadas por fecha 
print("Promedio por fecha del campo IB Calls\n")
df_promedio3 = df.groupby('Date')['IB Calls'].mean().reset_index()
print(df_promedio3,"\n")

print("Promedio por fecha del campo IB Handled\n")
df_promedio3 = df.groupby('Date')['IB Handled'].mean().reset_index()
print(df_promedio3,"\n")

#Promedio de llamadas por intervalos de tiempo 
print("Promedio por Intervalos de tiempo del campo IB Calls\n")
Intervalos = df.groupby("Interval")
Promedios = Intervalos["IB Calls"].mean()
Promedios1 = Intervalos["IB Handled"].mean()
df["Interval"] = pd.to_datetime(df["Interval"])
df["Interval"] = df["Interval"].apply(lambda x: x.strftime("%H:%M:%S").replace(":0", ":", ":") if len(x.strftime("%H:%M:%S")) == 6 else x.strftime("%H:%M:%S"))
df_ordenado = df.sort_values(by=["Interval"])
print(Promedios,"\n")

print("Promedio por Intervalos de tiempo del campo IB Handled\n")
print(Promedios1,"\n")

#Mostrar los resultados de determinado año (2023) en un gráfico de linea de tiempo 
df["Date"] = pd.to_datetime(df["Date"]).dt.date
Fecha_inicial = pd.to_datetime("2023-01-01").date()
Fecha_final = pd.to_datetime("2023-01-31").date()
Filas_Fecha = df[(df["Date"] >= Fecha_inicial) & (df["Date"] <= Fecha_final)]
Promedio_enero_c = Filas_Fecha.groupby("Date")["IB Calls"].mean().reset_index()
Promedio_enero_h = Filas_Fecha.groupby("Date")["IB Handled"].mean().reset_index()

plt.figure(figsize=(20,7))
plt.plot(Promedio_enero_c['Date'], Promedio_enero_c['IB Calls'], color = "blue", label='IB Calls')
plt.plot(Promedio_enero_h['Date'], Promedio_enero_h['IB Handled'], color = "orange", label='IB Handled')
plt.legend()
plt.xlabel('Date')
plt.ylabel('Promedio')
plt.title('Promedio de IB Calls e IB Handled en el mes de enero de 2023')
plt.show()

#Sacar el porcentaje del nivel de servicio 
Suma_IB_Calls= df["IB Calls"].sum()
Suma_Calls_SL= df["Calls in SL"].sum()
Result = round(Suma_Calls_SL/Suma_IB_Calls,2)
Result_porcentual = round(Suma_Calls_SL/Suma_IB_Calls*100,2)
print("El cumplimiento de nivel de servicio es:", Result)
print("El cumplimiento porcentual de nivel de servicio es:", Result_porcentual,"%")

#Gráfico de dispersión para un mes y año determinado (septiembre - 2022) 
df ["Date"] = pd.to_datetime(df["Date"])
Septiembre_2022 = df[(df["Date"].dt.year == 2022) & (df["Date"].dt.month == 9)]
IB_Calls_Sept_2022 = Septiembre_2022.groupby(Septiembre_2022["Date"])["IB Calls"].sum()
plt.figure(figsize=(20,7))
plt.scatter(IB_Calls_Sept_2022.index, IB_Calls_Sept_2022.values)
plt.title('IB Calls en Septiembre')
plt.xlabel('Día')
plt.ylabel('IB Calls')
plt.show()
print("\n",IB_Calls_Sept_2022)

#Gráfico comparativo entre métricas (Volumen de llamadas y nivel de servicio)
df ["Date"] = pd.to_datetime(df["Date"])
Septiembre_2022 = df[(df["Date"].dt.year == 2022) & (df["Date"].dt.month == 9)]
IB_Calls_Sept_2022 = Septiembre_2022.groupby('Date')["IB Calls"].sum()
IB_Calls_Sept_2022c = IB_Calls_Sept_2022.sum()
Calls_in_SL_Sept_2022 = Septiembre_2022.groupby("Date")["Calls in SL"].sum()
Calls_in_SL_Sept_2022s = Calls_in_SL_Sept_2022.sum()
print("El volumen de llamdas para el mes de septiembre de 2022 es:",IB_Calls_Sept_2022c)
print("El nivel de servicio para el mes de septiembre de 2022 es:",Calls_in_SL_Sept_2022s)

valores = [IB_Calls_Sept_2022c, Calls_in_SL_Sept_2022s]
etiquetas = ['Volumen de llamadas IB Calls', 'Nivel de servicio Calls in SL']
fig, ax = plt.subplots(figsize=(10,7))
ax.barh(etiquetas, valores, color='pink')
ax.set_xlabel('Valor')
ax.set_ylabel('Categoria')
plt.show()

#Marco de datos ponderados por mes en el año 2021 para una métrica determianada (IB AHT) 
df['Date'] = pd.to_datetime(df['Date'])
IB_AHT_2021 = df[(df["Date"].dt.year == 2021)]
df['Mes'] = df['Date'].dt.month 
print("Ponderados del año 2021 \n")
IB_2021 = IB_AHT_2021.groupby("Mes")["IB AHT"].count()
IB_2021I = IB_2021.sum()
print(IB_2021,"\n")
print("La cuenta total de IB AHT ES de:",IB_2021I,"\n")
Result = round(IB_2021/IB_2021I)
Result_porcentual = round(IB_2021/IB_2021I*100,2)
print("El porcentaje ponderado es:\n\n", Result_porcentual,"%")

#Gráfico de datos ponderados 

Meses = ['Enero', 'Febrero', 'Marzo', 'Abril','Mayo', 'Junio','Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

Ponderado = [9.58, 8.30, 9.10, 9.47, 8.90, 9.09, 9.63, 9.49, 6.62, 6.06, 5.90, 7.86]

fig, ax = plt.subplots(figsize=(20,10))
ax.set_ylabel('Ponderación')
ax.set_title('Meses')
plt.bar(Meses, Ponderado)
plt.show()
