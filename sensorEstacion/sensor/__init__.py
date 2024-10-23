from datetime import datetime
import sqlite3
from flask import Flask, request
from flask_cors import CORS
def dict_factory(cursor, row):
   """Arma un diccionario con los valores de la fila."""
   fields = [column[0] for column in cursor.description]
   return {key: value for key, value in zip(fields, row)}

db_path = 'sensores.sqlite'
conn = sqlite3.connect(db_path)
conn.row_factory = dict_factory
# Ensure the table exists

with open("sensor/sensor.sql") as f:
    conn.executescript(f.read())

app = Flask(__name__)
CORS(app)  # Esto habilita CORS para todas las rutas


@app.route('/sensores', methods=('GET',))
def mostrarValores():
    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    res = conn.execute('''
                        SELECT * FROM Sensores 
                        LIMIT 1
                    ''') 
    valores = res.fetchone()
    conn.close()

    return valores


@app.route('/sensores', methods=('POST', ))
def cargarValor():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    temp = float(request.form['tempDHT'])
    print(f'Sensor Temperatura: {temp}')
    hum = float(request.form['humDHT'])
    press = float(request.form['presionBMP'])
    light = float(request.form['luzLDR'])
    water = float(request.form['nivelAgua'])
    conn = sqlite3.connect(db_path)
    conn.execute('''
                        INSERT INTO Sensores (timestamp, temperature, humidity, pressure, lightLevel, waterLevel)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (timestamp, temp, hum, press, light, water)) 
    conn.commit()    
    conn.close()

    print( f"""Sensor Temperatura: {temp}
                Sensor Humedad: {hum}
                Sensor Presion: {press}
                Sensor Luz: {light}
                Sensor Agua: {water}

            """)

    return f"""Sensor Temperatura: {temp}
                Sensor Humedad: {hum}
                Sensor Presion: {press}
                Sensor Luz: {light}
                Sensor Agua: {water}

            """


