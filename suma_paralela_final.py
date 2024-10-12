import threading
import mysql.connector
from tqdm import tqdm

def conectar_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="suma_paralela"
    )

def sumar_parcial(desde, hasta, indice, resultados_parciales, pbars):
    conexion = conectar_mysql()
    cursor = conexion.cursor()
    query = f"SELECT valor FROM datos WHERE id BETWEEN {desde} AND {hasta};"
    cursor.execute(query) 
    resultado_parcial = 0
    for valor in cursor:
        resultado_parcial += valor[0]
        pbars[indice].update(1) 
    
    resultados_parciales[indice] = resultado_parcial

    cursor.close()
    conexion.close()

def main():
    total_datos = 1000000
    num_hilos = 10 
    tamaño_grupo = total_datos // num_hilos

    resultados_parciales = [0] * num_hilos  

    pbars = []
    for i in range(num_hilos):  
        pbar = tqdm(total=tamaño_grupo, desc=f"Hilo {i+1}", position=i, leave=True)
        pbars.append(pbar)

    hilos = []
    for i in range(num_hilos): 
        desde = i * tamaño_grupo + 1
        hasta = (i + 1) * tamaño_grupo
        hilo = threading.Thread(target=sumar_parcial, args=(desde, hasta, i, resultados_parciales, pbars))
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

    for pbar in pbars:
        pbar.close()

    suma_total = sum(resultados_parciales)

    print("Resultados parciales:", resultados_parciales)
    print("Suma total:", suma_total)

if __name__ == "__main__":
    main()
