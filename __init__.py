from flask import Flask

app = Flask(__name__)

@app.route('/temperatura')
def hello():
    return 'Sensor Temperatura: '