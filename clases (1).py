import pandas as pd
import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np
import os

# 1. VALIDACIÓN NUMÉRICA (Requerimiento 1)
# Sustentación: El profesor pide funciones de validación. 
# Esto evita que el programa se caiga si el usuario ingresa una letra en lugar de un número.
def validar_int(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: Por favor ingresa un número entero válido.")

# 2. CLASE BASE (Abstracción)
# Sustentación: Usamos POO para que Archivo sea la 'plantilla' general.
class Archivo:
    def __init__(self, ruta):
        self._ruta = ruta  # Atributo protegido (encapsulamiento)
        self.data = None

# 3. CLASE PARA ARCHIVOS SIATA (Requerimiento 5 y 6)
class ArchivoCSV(Archivo):
    def cargar(self):
        self.data = pd.read_csv(self._ruta)
        if not os.path.isfile(self._ruta):
            print(f" Error: '{self._ruta}' no es un archivo válido o no existe.")
            print("   Asegúrate de incluir el nombre del archivo (ej: datos.csv)")
            return

        # Verificar extensión
        if not self._ruta.endswith('.csv'):
            print(f" Advertencia: El archivo '{self._ruta}' no parece ser un CSV.")

        try:
            self.data = pd.read_csv(self._ruta)
            print(f" Archivo cargado exitosamente: {os.path.basename(self._ruta)}")
            print(self.data.info())
            print(self.data.describe())
        except Exception as e:
            print(f" Error al leer el archivo: {e}")
        # Requerimiento 5: info() y describe() [cite: 13]
        print(self.data.info())
        print(self.data.describe())

    def graficas(self, columna):
        if columna not in self.data.columns:
            print(f" Columna '{columna}' no existe. Columnas disponibles: {list(self.data.columns)}")
            return

    # Eliminar valores NaN y asegurar tipo numérico
        datos_limpios = self.data[columna].dropna()
        if datos_limpios.empty:
            print(f" La columna '{columna}' no tiene datos válidos después de eliminar NaN.")
            return

        fig, axs = plt.subplots(3, 1, figsize=(7, 10))
        
        # Gráfico de línea (usando índice actual, puede ser numérico o fechas)
        datos_limpios.plot(ax=axs[0], title=f"Evolución de {columna}")
        axs[0].set_ylabel("Valor")
        
        # Boxplot
        datos_limpios.plot.box(ax=axs[1], title=f"Boxplot de {columna}")
        axs[1].set_ylabel("Valor")
        
        # Histograma
        datos_limpios.hist(ax=axs[2], bins=20)
        axs[2].set_title(f"Histograma de {columna}")
        axs[2].set_xlabel("Valor")
    
        plt.tight_layout()
        plt.savefig(f"graficas_siata_{columna}.png")
        plt.show()

    def operaciones(self, col1, col2):
        # Requerimiento 5: apply, map y operación aritmética [cite: 13]
        self.data["Doble"] = self.data[col1].apply(lambda x: x * 2) # Operación elegida 1
        self.data["Incremento"] = self.data[col1].map(lambda x: x + 10) # Operación elegida 2
        self.data["Resultado_Suma"] = self.data[col1] + self.data[col2] # Sumar columnas
        print(self.data.head())

    def procesamiento_fechas(self, col_fecha):
        # Requerimiento 6: Resample a días, meses y trimestres [cite: 14]
        self.data[col_fecha] = pd.to_datetime(self.data[col_fecha])
        self.data.set_index(col_fecha, inplace=True)
        
        for periodo, nombre in [('D', 'Diario'), ('M', 'Mensual'), ('Q', 'Trimestral')]:
            # numeric_only=True evita errores con texto al promediar
            resumen = self.data.resample(periodo).mean(numeric_only=True)
            resumen.plot(title=f"Datos Remuestreados: {nombre}")
            plt.savefig(f"resample_{nombre}.png")
            plt.show()

# 4. CLASE PARA ARCHIVOS EEG (Requerimiento 7)
class ArchivoMAT(Archivo):
    def cargar(self):
        # Requerimiento 7: mostrar llaves con whosmat [cite: 16]
        print("Estructura del archivo:", sio.whosmat(self._ruta))
        self.data = sio.loadmat(self._ruta)

    def sumar_3_canales(self, nombre_matriz, c1, c2, c3, p_min, p_max):
        # Requerimiento 7a: Convertir a 2D y sumar canales en rango [cite: 17, 19]
        matriz_2d = np.squeeze(self.data[nombre_matriz]) # Quitamos dimensiones extra
        segmento = matriz_2d[p_min:p_max, :]
        suma = segmento[:, c1] + segmento[:, c2] + segmento[:, c3]
        
        # Unidades: 1kHz = 1ms por muestra. [cite: 16]
        tiempo = np.arange(p_min, p_max) / 1000 

        fig, (ax1, ax2) = plt.subplots(2, 1)
        ax1.plot(tiempo, segmento[:, c1], label=f"Canal {c1}")
        ax1.plot(tiempo, segmento[:, c2], label=f"Canal {c2}")
        ax1.plot(tiempo, segmento[:, c3], label=f"Canal {c3}")
        ax1.set_ylabel("Microvoltios (uV)") # Unidades [cite: 18, 22]
        ax1.legend()

        ax2.plot(tiempo, suma, color='r', label="Suma")
        ax2.set_xlabel("Segundos (s)")
        ax2.set_ylabel("Microvoltios (uV)")
        ax2.legend()
        
        plt.savefig("suma_eeg.png") # Guardar como png/jpg [cite: 19]
        plt.show()

    def estadisticas_3d(self, nombre_matriz):
        # Requerimiento 7b: Operar sobre matriz 3D original [cite: 20]
        matriz_3d = self.data[nombre_matriz] 
        prom = np.mean(matriz_3d, axis=0).flatten() # Promedio a lo largo de un eje
        desv = np.std(matriz_3d, axis=0).flatten()

        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.stem(prom)
        ax1.set_title("Promedio")
        ax2.stem(desv)
        ax2.set_title("Desviación Estándar")
        plt.show()

# 5. CLASE GESTOR (Puntos Extra) [cite: 21]
class GestorObjetos:
    def __init__(self):
        self.inventario = []
    def guardar(self, obj):
        self.inventario.append(obj)
    def buscar_por_tipo(self, clase):
        return [o for o in self.inventario if isinstance(o, clase)]