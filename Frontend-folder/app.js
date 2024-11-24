const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();

// Set EJS as the template engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Serve static files from the public directory
app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Routes
app.get('/', (req, res) => res.render('index'));

app.get('/investors', async (req, res) => {
  try {
    console.log("DEBUG: Fetching investors...");
    const response = await axios.get('http://127.0.0.1:5000/api/investors');
    console.log("DEBUG: Investors fetched:", response.data);
    res.render('investors', { investors: response.data });
  } catch (error) {
    console.error('Error fetching investors:', error.message || error);
    if (error.response) {
      console.error('Response:', error.response.status, error.response.data);
    }
    res.render('error', { message: 'Failed to load investors.' });
  }
});


app.get('/stocks', async (req, res) => {
  try {
    console.log("DEBUG: Fetching stocks from backend...");
    const response = await axios.get('http://127.0.0.1:5000/api/stocks');
    console.log("DEBUG: Stocks fetched successfully:", response.data);
    res.render('stocks', { stocks: response.data });
  } catch (error) {
    console.error("DEBUG: Error fetching stocks:", error.message || error);
    if (error.response) {
      console.error("DEBUG: Response status:", error.response.status);
      console.error("DEBUG: Response data:", error.response.data);
    }
    res.render('error', { message: 'Failed to load stocks.' });
  }
});


app.get('/bonds', async (req, res) => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/bonds'); // Backend API
    res.render('bonds', { bonds: response.data });
  } catch (error) {
    console.error(error);
    res.render('error', { message: 'Failed to load bonds.' });
  }
});

app.get('/portfolio', async (req, res) => {
  try {
    const investorId = req.query.investorId; // Example query param
    const response = await axios.get(`http://localhost:5000/api/investor/${investorId}/portfolio`); // Backend API
    res.render('portfolio', { portfolio: response.data });
  } catch (error) {
    console.error(error);
    res.render('error', { message: 'Failed to load portfolio.' });
  }
});


app.listen(3000, () => {
  console.log('Frontend server running on http://localhost:3000');
});
