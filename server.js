const express = require('express');
const fetch = require('node-fetch');
const cors = require('cors');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

const DFS_LOGIN = process.env.DFS_LOGIN || 'zeidyseo@gmail.com';
const DFS_PASS = process.env.DFS_PASS || 'd7f16797ed57a345';
const AUTH = 'Basic ' + Buffer.from(DFS_LOGIN + ':' + DFS_PASS).toString('base64');

// SERP API - Google Organic
app.post('/api/serp', async (req, res) => {
  try {
    const response = await fetch('https://api.dataforseo.com/v3/serp/google/organic/live/advanced', {
      method: 'POST',
      headers: { 'Authorization': AUTH, 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body)
    });
    const data = await response.json();
    res.json(data);
  } catch (err) {
    console.error('SERP error:', err.message);
    res.status(500).json({ error: err.message });
  }
});

// OnPage API - Technical audit
app.post('/api/onpage', async (req, res) => {
  try {
    const response = await fetch('https://api.dataforseo.com/v3/on_page/instant_pages', {
      method: 'POST',
      headers: { 'Authorization': AUTH, 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body)
    });
    const data = await response.json();
    res.json(data);
  } catch (err) {
    console.error('OnPage error:', err.message);
    res.status(500).json({ error: err.message });
  }
});

// Backlinks API
app.post('/api/backlinks', async (req, res) => {
  try {
    const response = await fetch('https://api.dataforseo.com/v3/backlinks/summary/live', {
      method: 'POST',
      headers: { 'Authorization': AUTH, 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body)
    });
    const data = await response.json();
    res.json(data);
  } catch (err) {
    console.error('Backlinks error:', err.message);
    res.status(500).json({ error: err.message });
  }
});

// PageSpeed proxy
app.get('/api/pagespeed', async (req, res) => {
  try {
    const { url, strategy } = req.query;
    const response = await fetch(
      `https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=${encodeURIComponent(url)}&strategy=${strategy}`
    );
    const data = await response.json();
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Google Maps / Business Data
app.post('/api/maps', async (req, res) => {
  try {
    const response = await fetch('https://api.dataforseo.com/v3/serp/google/maps/live/advanced', {
      method: 'POST',
      headers: { 'Authorization': AUTH, 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body)
    });
    const data = await response.json();
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Zeidy SEO Tool running on port ${PORT}`));
