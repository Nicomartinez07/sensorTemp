import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './WeatherDashboard.css';
import { FaMoon } from 'react-icons/fa';
import { FiSun, FiSunrise, FiSunset } from "react-icons/fi";
import { WiHumidity, WiDayRain, WiNightAltRain } from "react-icons/wi";

const WeatherDashboard = () => {
  const [data, setData] = useState({
    temperature: null,
    humidity: null,
    pressure: null,
    lightLevel: null,
    timestamp: null,
    waterLevel: null,
    sunrise: null,
    sunset: null,
  });

  // Función para obtener los datos desde la API
  const fetchData = () => {
    axios.get('http://10.9.121.202:5000/sensores')
      .then(response => {
        console.log("Datos recibidos:", response.data); // Mostrar los datos recibidos
        setData(response.data); // Actualiza el estado con los datos recibidos
      })
      .catch(error => {
        console.error('Error al obtener los datos:', error);
      });
  };

  // Efecto para obtener los datos inicialmente y cada minuto
  useEffect(() => {
    // Llamada inicial a la API
    fetchData();

    // Establecer un intervalo para actualizar los datos cada minuto (60000 ms)
    const interval = setInterval(fetchData, 60000);

    // Limpiar el intervalo cuando el componente se desmonte
    return () => clearInterval(interval);
  }, []);

  // Efecto para cambiar el fondo y el ícono según el nivel de luz
  const isDay = data.lightLevel && data.lightLevel >= 350; // Verificación de luz solo aquí

  useEffect(() => {
    if (data.lightLevel !== null) {
      if (isDay) {
        document.body.classList.add('light-mode');
        document.body.classList.remove('dark-mode');
      } else {
        document.body.classList.add('dark-mode');
        document.body.classList.remove('light-mode');
      }
    }
  }, [isDay]); // Solo dependemos de isDay aquí

  // Función para formatear la fecha y la hora
  const formatDateTime = (timestamp) => {
    if (!timestamp) return null;
    const dateObj = new Date(timestamp);
    const date = dateObj.toLocaleDateString('es-ES');
    const time = dateObj.toLocaleTimeString('es-ES', {
      hour: '2-digit',
      minute: '2-digit',
    });
    return { date, time };
  };

  const formattedDateTime = formatDateTime(data.timestamp);

  // Lógica para mostrar el icono de lluvia si el nivel de agua es mayor a 80
  const rainIcon = data.waterLevel > 80 ? (
    isDay ? (
      <WiDayRain className="weather-icon rain-icon" style={{ color: 'blue' }} /> // Ícono de lluvia de día con color azul
    ) : (
      <WiNightAltRain className="weather-icon rain-icon" style={{ color: 'darkblue' }} /> // Ícono de lluvia de noche con color azul oscuro
    )
  ) : (
    isDay ? <FiSun className="weather-icon sun-icon" /> : <FaMoon className="weather-icon moon-icon" />
  );

  return (
    <div className="dashboard">
      <header className="header">
        <h1>Temperatura en la ETEC:</h1>
        {formattedDateTime && (
          <p className="timestamp">{formattedDateTime.time} - {formattedDateTime.date}</p>
        )}
      </header>
      <div className="temperature-display">
        {rainIcon} {/* Aquí se muestra el ícono de lluvia o de sol/luna */}
        <span className="temperature">{data.temperature ? `${data.temperature}°` : 'Cargando...'}</span>
      </div>

      <div className="info-grid">
        <div className="info-card"><WiHumidity className="humidity-icon" />Humedad: {data.humidity ? `${data.humidity}%` : 'Cargando...'}</div>
        <div className="info-card">Presión: {data.pressure ? `${data.pressure} hPa` : 'Cargando...'}</div>
        
        {/* Mostrar la hora de salida y puesta del sol */}
        <div className="info-card">
          <FiSunrise style={{ color: 'yellow', marginRight: '8px' }} /> Salida del sol: {data.sunrise ? new Date(data.sunrise).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' }) : 'Cargando...'}
        </div>
        <div className="info-card">
          <FiSunset style={{ color: 'orange', marginRight: '8px' }} /> Atardecer: {data.sunset ? new Date(data.sunset).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' }) : 'Cargando...'}
        </div>
      </div>

      <footer className="footer">
        <p>Hecho por: <a href="https://github.com/Nicomartinez07">Nicolas Martinez</a></p>
      </footer>
    </div>
  );
};

export default WeatherDashboard;
