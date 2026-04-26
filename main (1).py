from clases import ArchivoCSV, ArchivoMAT, GestorObjetos, validar_int

def menu():
    gestor = GestorObjetos() # Sistema de almacenamiento (puntos extra)
    
    while True:
        print("\n--- SISTEMA NEUROAMBIENTAL ---")
        print("1. Cargar Archivo CSV (SIATA)")
        print("2. Cargar Archivo MAT (EEG)")
        print("3. Ver objetos guardados (Gestor)")
        print("4. Salir")
        
        op = input("Seleccione: ")
        
        if op == "1":
            ruta = input("Ruta del CSV: ")
            obj = ArchivoCSV(ruta)
            obj.cargar()
            print(" Columnas disponibles:", list(obj.data.columns))
            col = input("Nombre de la columna para graficar: ")
            obj.graficas(col)
            obj.operaciones(col, col) # Ejemplo usando la misma columna
            fec = input("Nombre de la columna de fecha: ")
            obj.procesamiento_fechas(fec)
            gestor.guardar(obj)

        elif op == "2":
            ruta = input("Ruta del MAT: ")
            obj = ArchivoMAT(ruta)
            obj.cargar()
            key = input("Nombre de la matriz (visto en whosmat): ")
            
            print("a. Sumar 3 canales\nb. Estadísticas 3D")
            sub_op = input("Opción: ")
            if sub_op == "a":
                c1 = validar_int("Canal 1: "); c2 = validar_int("Canal 2: "); c3 = validar_int("Canal 3: ")
                p1 = validar_int("Punto inicio: "); p2 = validar_int("Punto fin: ")
                obj.sumar_3_canales(key, c1, c2, c3, p1, p2)
            else:
                obj.estadisticas_3d(key)
            gestor.guardar(obj)

        elif op == "3":
            print(f"Total objetos: {len(gestor.inventario)}")

        elif op == "4":
            break

if __name__ == "__main__":
    menu()