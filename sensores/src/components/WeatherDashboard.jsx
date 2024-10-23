import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './WeatherDashboard.css';

const WeatherDashboard = () => {
  // Estado para guardar los datos que provienen de la base de datos
  const [data, setData] = useState({
    temperature: null,
    humidity: null,
    pressure: null,
    lightLevel: null,
    timestamp: null,
    waterLevel: null,
  });

  // Efecto para obtener los datos desde la API
  useEffect(() => {
    axios.get('http://10.9.121.112:5000/sensores')
      .then(response => {
        console.log(response.data)
        setData(response.data); // Actualiza el estado con los datos recibidos
      })
      .catch(error => {
        console.error('Error al obtener los datos:', error);
      });
  }, []);

  return (
    <div className="dashboard">
      <header className="header">
        <h1>Temperatura en la etec:</h1>
      </header>

      <div className="info-grid">
        <div className="info-card">Temperatura: {data.temperature ? `${data.temperature} °C` : 'Cargando...'}</div>
        <div className="info-card">Humedad: {data.humidity ? `${data.humidity}%` : 'Cargando...'}</div>
        <div className="info-card">Presión: {data.pressure ? `${data.pressure} mb` : 'Cargando...'}</div>
        <div className="info-card">Luz: {data.lightLevel ? `${data.lightLevel} lux` : 'Cargando...'}</div>
        <div className="info-card">Nivel de agua: {data.waterLevel ? `${data.waterLevel}` : 'Cargando...'}</div>
        <div className="info-card">Fecha: {data.timestamp ? `${data.timestamp}` : 'Cargando...'}</div>
        <div className="info-card">Salida del sol: 06:01</div>
        <div className="info-card">Atardecer: 19:15</div>
      </div>

      <footer className="footer">
        <p>Hecho por: <a href="https://github.com/Nicomartinez07">Nicolas Martinez</a></p>
      </footer>
    </div>
  );
};

export default WeatherDashboard;


