const express = require('express');
const fetch = require('node-fetch');
const cors = require('cors');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

const SERP_API_KEY = process.env.SERP_API_KEY || 'D2DF82D01D1E4BD8A9A301DDF3BC7217';
const DFS_LOGIN = process.env.DFS_LOGIN || 'zeidyseo@gmail.com';
const DFS_PASS = process.env.DFS_PASS || 'd7f16797ed57a345';
const DFS_AUTH = 'Basic ' + Buffer.from(DFS_LOGIN + ':' + DFS_PASS).toString('base64');

// Country code mapping for SerpApi
const COUNTRY_GL = {
  '2682': 'sa', '2784': 'ae', '2414': 'kw',
  '2634': 'qa', '2048': 'bh', '2512': 'om',
  '65': 'eg', '2036': 'jo'
};

// SERP via SerpApi
app.post('/api/serp', async (req, res) => {
  try {
    const body = req.body[0];
    const gl = COUNTRY_GL[String(body.location_code)] || 'sa';
    const start = body.offset || 0;

    const url = `https://serpapi.com/search.json?engine=google&q=${encodeURIComponent(body.keyword)}&gl=${gl}&hl=ar&num=10&start=${start}&api_key=${SERP_API_KEY}`;

    const response = await fetch(url);
    const data = await response.json();

    // Transform SerpApi response to match expected format
    const items = (data.organic_results || []).map((r, i) => ({
      type: 'organic',
      rank_absolute: start + i + 1,
      title: r.title || '',
      url: r.link || '',
      domain: r.displayed_link ? r.displayed_link.replace(/^https?:\/\//, '').split('/')[0] : new URL(r.link || 'https://x.com').hostname,
      description: r.snippet || ''
    }));

    res.json({
      tasks: [{
        status_code: 20000,
        status_message: 'Ok',
        result: [{ items }]
      }]
    });
  } catch (err) {
    console.error('SERP error:', err.message);
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

// Backlinks via DataForSEO (when activated)
app.post('/api/backlinks', async (req, res) => {
  try {
    const response = await fetch('https://api.dataforseo.com/v3/backlinks/summary/live', {
      method: 'POST',
      headers: { 'Authorization': DFS_AUTH, 'Content-Type': 'application/json' },
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
