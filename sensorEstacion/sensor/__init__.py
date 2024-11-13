from datetime import datetime
import sqlite3
import requests
from flask import Flask, request
from flask_cors import CORS

def dict_factory(cursor, row):
   """Arma un diccionario con los valores de la fila."""
   fields = [column[0] for column in cursor.description]
   return {key: value for key, value in zip(fields, row)}

# Ruta a la base de datos
db_path = 'sensores.sqlite'

# Conexión inicial a la base de datos
conn = sqlite3.connect(db_path)
conn.row_factory = dict_factory

# Asegurarse de que la tabla exista (suponiendo que ya creaste la base)
with open("sensor/sensor.sql") as f:
    conn.executescript(f.read())
conn.close()

# Inicializar Flask
app = Flask(__name__)
CORS(app)  # Esto habilita CORS para todas las rutas

# Función para obtener los tiempos de salida y puesta del sol desde la API
def obtener_tiempos_sol(lat, lon):
    url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&formatted=0"
    respuesta = requests.get(url)
    datos = respuesta.json()

    if respuesta.status_code == 200:
        sunrise = datos["results"]["sunrise"]
        sunset = datos["results"]["sunset"]
        return sunrise, sunset
    else:
        print("Error al obtener los tiempos del sol")
        return None, None

@app.route('/sensores', methods=('GET',))
def mostrarValores():
    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    res = conn.execute('''
                        SELECT * FROM Sensores 
                        ORDER BY timestamp DESC
                        LIMIT 1
                    ''') 
    valores = res.fetchone()
    conn.close()

    return valores


@app.route('/sensores', methods=('POST', ))
def cargarValor():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    temp = float(request.form['tempDHT'])
    hum = float(request.form['humDHT'])
    press = float(request.form['presionBMP'])
    light = float(request.form['luzLDR'])
    water = float(request.form['nivelAgua'])

    # Definir las coordenadas de la ubicación
    lat = -34.603722  # Ejemplo: latitud de Buenos Aires
    lon =  -58.381592  # Ejemplo: longitud de Buenos Aires

    # Obtener los tiempos de salida y puesta del sol
    sunrise, sunset = obtener_tiempos_sol(lat, lon)
    
    # Si los tiempos se obtienen correctamente
    if sunrise and sunset:
        print(f"Hora de salida del sol: {sunrise}")
        print(f"Hora de puesta del sol: {sunset}")
    else:
        print("Error al obtener los tiempos del sol.")
    
    # Guardar los datos en la base de datos
    conn = sqlite3.connect(db_path)
    conn.execute('''
        INSERT INTO Sensores (timestamp, temperature, humidity, pressure, lightLevel, waterLevel, sunrise, sunset)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (timestamp, temp, hum, press, light, water, sunrise, sunset)) 
    conn.commit()    
    conn.close()

    print(f"""Sensor Temperatura: {temp}
                Sensor Humedad: {hum}
                Sensor Presión: {press}
                Sensor Luz: {light}
                Sensor Agua: {water}
                Hora de salida del sol: {sunrise}
                Hora de puesta del sol: {sunset}
            """)

    return f"""Sensor Temperatura: {temp}
                Sensor Humedad: {hum}
                Sensor Presión: {press}
                Sensor Luz: {light}
                Sensor Agua: {water}
                Hora de salida del sol: {sunrise}
                Hora de puesta del sol: {sunset}
            """
