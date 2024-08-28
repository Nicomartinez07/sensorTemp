from flask import Flask, request

app = Flask(__name__)

@app.route('/temperatura', methods=('POST',))
def hello():
    temp = request.form['sensor']
    return f'Sensor Temperatura: {temp}'