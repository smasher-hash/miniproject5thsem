const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
const PORT = 3000;

// Enable CORS for all origins (for development)
app.use(cors());

// Replace with your own OpenWeatherMap API key
const API_KEY = '752fc0190efdd1f0ef72acf67beb5565';

app.get('/api/weather', async (req, res) => {
  const village = req.query.village || 'Delhi'; // default fallback

  try {
    const response = await axios.get(
      `https://api.openweathermap.org/data/2.5/weather?q=${village}&appid=${API_KEY}&units=metric`
    );

    const weather = response.data;
    const description = weather.weather[0].description;
    const temp = weather.main.temp;
    const alert = temp > 38 ? 'Heatwave Warning' : temp < 5 ? 'Cold Alert' : null;

    res.json({
      description: `${description}, ${temp}°C`,
      alert: alert
    });
  } catch (error) {
    console.error(error.message);
    res.status(500).json({ error: 'Unable to fetch weather data' });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
