from datetime import datetime
import sqlite3
from flask import Flask, request

db_path = 'sensores.sqlite'
conn = sqlite3.connect(db_path)
# Ensure the table exists

with open("sensores.sql") as f:
    conn.executescript(f.read())

app = Flask(__name__)

@app.route('/sensores', methods=('POST',))
def hello():
    temp = float(request.form['sensor'])
    print(f'Sensor Temperatura: {temp}')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hum = float(request.form['sensor'])
    press = float(request.form['sensor'])
    light = float(request.form['sensor'])
    water = float(request.form['sensor'])
    conn = sqlite3.connect(db_path)
    conn.execute('''
                        INSERT INTO TemperatureData (timestamp, temperature, humidity, pressure, lightLevel, waterLevel)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (timestamp, temp, humidity, pressure, lightLevel, waterLevel)) 
    conn.commit()    
    conn.close()
    return f'Sensor Temperatura: {temp}'