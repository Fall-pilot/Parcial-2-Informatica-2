# ------------------ IMPORTACIONES ------------------
import pandas as pd
import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np

# ================= Clase base =================
class Archivo:
    def __init__(self, ruta):
        self._ruta = ruta  # Atributo protegido
        self.data = None

    def cargar(self):
        pass

# ================= CLASE CSV =================
class ArchivoCSV(Archivo):
    def __init__(self, ruta):
        super().__init__(ruta)

    def cargar(self):
        self.data = pd.read_csv(self._ruta)
        print("--- Info del Archivo ---")
        print(self.data.info())
        print("\n--- Estadísticas ---")
        print(self.data.describe())

    def graficas(self, columna):
        fig, axs = plt.subplots(3, 1, figsize=(8, 10))

        self.data[columna].plot(ax=axs[0], title="Gráfico de Línea")
        self.data[columna].plot.box(ax=axs[1], title="Boxplot (Caja y Bigotes)")
        self.data[columna].hist(ax=axs[2], bins=20)
        axs[2].set_title("Histograma")

        plt.tight_layout()
        plt.savefig("graficas_csv.png") # PRIMERO GUARDAR
        plt.show()                       # LUEGO MOSTRAR

    def operaciones(self, col1, col2):
        self.data["apply"] = self.data[col1].apply(lambda x: x * 2)
        self.data["map"] = self.data[col1].map(lambda x: x + 1)
        self.data["suma"] = self.data[col1] + self.data[col2]
        print(self.data.head())

    def fechas(self, columna_fecha):
        self.data[columna_fecha] = pd.to_datetime(self.data[columna_fecha])
        self.data.set_index(columna_fecha, inplace=True)

        # Usamos numeric_only=True para evitar errores con columnas de texto
        for periodo, nombre in [("D", "diario"), ("M", "mensual"), ("Q", "trimestral")]:
            self.data.resample(periodo).mean(numeric_only=True).plot(title=f"Resumen {nombre}")
            plt.savefig(f"{nombre}.png")
            plt.show()

# ================= CLASE MAT =================
class ArchivoMAT(Archivo):
    def __init__(self, ruta):
        super().__init__(ruta)

    def cargar(self):
        print("Variables en el archivo MAT:", sio.whosmat(self._ruta))
        self.data = sio.loadmat(self._ruta)

    def sumar_canales(self, matriz, c1, c2, c3, inicio, fin):
        # Aseguramos que trabajamos con un trozo de la matriz
        segmento = matriz[inicio:fin, :]
        suma = segmento[:, c1] + segmento[:, c2] + segmento[:, c3]

        plt.figure(figsize=(10, 6))
        plt.subplot(2,1,1)
        plt.plot(segmento[:, c1], label="Canal 1")
        plt.plot(segmento[:, c2], label="Canal 2")
        plt.plot(segmento[:, c3], label="Canal 3")
        plt.legend()

        plt.subplot(2,1,2)
        plt.plot(suma, label="Suma de Canales", color='red')
        plt.legend()

        plt.savefig("suma_canales.png")
        plt.show()

    def estadisticas(self, matriz):
        promedio = np.mean(matriz, axis=0)
        desviacion = np.std(matriz, axis=0)

        plt.figure(figsize=(10, 4))
        plt.subplot(1,2,1)
        # Agregamos range() para evitar errores de dimensiones
        plt.stem(range(len(promedio)), promedio)
        plt.title("Promedio por Canal")

        plt.subplot(1,2,2)
        plt.stem(range(len(desviacion)), desviacion)
        plt.title("Desviación por Canal")

        plt.savefig("estadisticas.png")
        plt.show()

# ================= CLASE GESTOR =================
class Gestor:
    def __init__(self):
        self.objetos = []

    def agregar(self, obj):
        self.objetos.append(obj)

    def buscar(self, tipo):
        return [o for o in self.objetos if isinstance(o, tipo)]

# ================= BLOQUE DE EJECUCIÓN (Para que aparezca el botón Play) =================
if __name__ == "__main__":
    print("El programa está listo. Define tus rutas y llama a los métodos aquí.")
    # Ejemplo:
    # mi_gestor = Gestor()
    # test_csv = ArchivoCSV("tus_datos.csv")
    # mi_gestor.agregar(test_csv)