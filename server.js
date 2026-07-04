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

// ⚠️ Credentials MUST come from Render Environment Variables (never hardcode them in a public repo)
const DFS_LOGIN = process.env.DFS_LOGIN;
const DFS_PASS = process.env.DFS_PASS;
const AUTH = 'Basic ' + Buffer.from(DFS_LOGIN + ':' + DFS_PASS).toString('base64');

// Generic DataForSEO proxy helper
async function dfsProxy(url, body, res) {
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Authorization': AUTH, 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });
    res.json(await response.json());
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}

// SERP API
app.post('/api/serp', (req, res) =>
  dfsProxy('https://api.dataforseo.com/v3/serp/google/organic/live/advanced', req.body, res));

// OnPage API
app.post('/api/onpage', (req, res) =>
  dfsProxy('https://api.dataforseo.com/v3/on_page/instant_pages', req.body, res));

// Backlinks API
app.post('/api/backlinks', (req, res) =>
  dfsProxy('https://api.dataforseo.com/v3/backlinks/summary/live', req.body, res));

// Google Maps API
app.post('/api/maps', (req, res) =>
  dfsProxy('https://api.dataforseo.com/v3/serp/google/maps/live/advanced', req.body, res));

// ===== NEW: Keyword Search Volume (Keywords Data API) =====
app.post('/api/volume', (req, res) =>
  dfsProxy('https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live', req.body, res));

// ===== NEW: Domain Rank Overview (DataForSEO Labs) =====
app.post('/api/domain-overview', (req, res) =>
  dfsProxy('https://api.dataforseo.com/v3/dataforseo_labs/google/domain_rank_overview/live', req.body, res));

// ===== NEW: Competitors (DataForSEO Labs) =====
app.post('/api/competitors', (req, res) =>
  dfsProxy('https://api.dataforseo.com/v3/dataforseo_labs/google/competitors_domain/live', req.body, res));

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
