const express = require('express');
const fetch = require('node-fetch');
const cors = require('cors');
const path = require('path');
const { execSync, spawn } = require('child_process');
const fs = require('fs');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

const DFS_LOGIN = process.env.DFS_LOGIN || 'zeidyseo@gmail.com';
const DFS_PASS = process.env.DFS_PASS || 'd7f16797ed57a345';
const AUTH = 'Basic ' + Buffer.from(DFS_LOGIN + ':' + DFS_PASS).toString('base64');

// SERP API
app.post('/api/serp', async (req, res) => {
  try {
    const response = await fetch('https://api.dataforseo.com/v3/serp/google/organic/live/advanced', {
      method: 'POST',
      headers: { 'Authorization': AUTH, 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body)
    });
    res.json(await response.json());
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// OnPage API
app.post('/api/onpage', async (req, res) => {
  try {
    const response = await fetch('https://api.dataforseo.com/v3/on_page/instant_pages', {
      method: 'POST',
      headers: { 'Authorization': AUTH, 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body)
    });
    res.json(await response.json());
  } catch (err) {
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
    res.json(await response.json());
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// PageSpeed API
app.get('/api/pagespeed', async (req, res) => {
  try {
    const { url, strategy } = req.query;
    const response = await fetch(
      `https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=${encodeURIComponent(url)}&strategy=${strategy}`
    );
    res.json(await response.json());
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Google Maps API
app.post('/api/maps', async (req, res) => {
  try {
    const response = await fetch('https://api.dataforseo.com/v3/serp/google/maps/live/advanced', {
      method: 'POST',
      headers: { 'Authorization': AUTH, 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body)
    });
    res.json(await response.json());
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// PDF Generation API
app.post('/api/pdf', async (req, res) => {
  try {
    const data = req.body;
    const tmpFile = `/tmp/report_${Date.now()}.json`;
    const pdfFile = `/tmp/report_${Date.now()}.pdf`;
    
    fs.writeFileSync(tmpFile, JSON.stringify(data));
    
    const pythonScript = `
import json, sys
sys.path.insert(0, '${__dirname}')
from generate_pdf import generate_pdf
with open('${tmpFile}') as f:
    data = json.load(f)
pdf_bytes, wa_msg = generate_pdf(data)
with open('${pdfFile}', 'wb') as f:
    f.write(pdf_bytes)
print(wa_msg)
`;
    
    const { execSync } = require('child_process');
    const wa_msg = execSync(`python3 -c "${pythonScript.replace(/"/g, '\\"').replace(/\n/g, ' ')}"`, {
      timeout: 30000
    }).toString().trim();
    
    const pdfBuffer = fs.readFileSync(pdfFile);
    
    // Cleanup
    fs.unlinkSync(tmpFile);
    fs.unlinkSync(pdfFile);
    
    res.set({
      'Content-Type': 'application/pdf',
      'Content-Disposition': `attachment; filename="zeidy-seo-${data.domain}.pdf"`,
      'X-WA-Message': Buffer.from(wa_msg).toString('base64')
    });
    res.send(pdfBuffer);
  } catch (err) {
    console.error('PDF error:', err.message);
    res.status(500).json({ error: err.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Zeidy SEO Tool running on port ${PORT}`));
