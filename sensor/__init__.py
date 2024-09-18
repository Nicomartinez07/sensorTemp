from datetime import datetime
import sqlite3
from flask import Flask, request

db_path = 'sensor.sqlite'
conn = sqlite3.connect(db_path)
# Ensure the table exists

with open("sensor.sql") as f:
    conn.executescript(f.read())

app = Flask(__name__)

@app.route('/temperatura', methods=('POST',))
def hello():
    temp = float(request.form['sensor'])
    print(f'Sensor Temperatura: {temp}')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(db_path)
    conn.execute('''
                        INSERT INTO TemperatureData (timestamp, temperature)
                        VALUES (?, ?)
                    ''', (timestamp, temp))
    conn.commit()    
    conn.close()
    return f'Sensor Temperatura: {temp}'