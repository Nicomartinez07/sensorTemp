from datetime import datetime
import sqlite3
from flask import Flask, request

db_path = 'sensores.sqlite'
conn = sqlite3.connect(db_path)
# Ensure the table exists

with open("sensor.sql") as f:
    conn.executescript(f.read())

app = Flask(__name__)

@app.route('/sensores', methods=('POST',))
def hello():
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


