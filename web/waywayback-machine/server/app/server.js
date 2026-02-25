const express = require('express');
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const https = require('https');
const http = require('http');
const sanitizeHtml = require('sanitize-html');

const app = express();
const PORT = 3000;

// Middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

// Store snapshots
const SNAPSHOTS_DIR = path.join(__dirname, 'snapshots');
if (!fs.existsSync(SNAPSHOTS_DIR)) {
  fs.mkdirSync(SNAPSHOTS_DIR, { recursive: true });
}

// In-memory snapshot status store
const snapshotStatuses = new Map();

// Generate unique ID
function generateId() {
  return crypto.randomBytes(8).toString('hex');
}

// Home page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Create snapshot endpoint - accepts URL to archive
app.post('/api/snapshot', async (req, res) => {
  try {
    const { url } = req.body;
    
    if (!url || typeof url !== 'string') {
      return res.status(400).json({ error: 'URL required' });
    }

    // Basic URL validation
    let targetUrl;
    try {
      targetUrl = new URL(url);
      if (!['http:', 'https:'].includes(targetUrl.protocol)) {
        return res.status(400).json({ error: 'Only HTTP/HTTPS URLs allowed' });
      }
    } catch (e) {
      return res.status(400).json({ error: 'Invalid URL format' });
    }

    console.log(`Creating snapshot for: ${url}`);
    
    // Generate snapshot ID
    const snapshotId = generateId();
    snapshotStatuses.set(snapshotId, { status: 'pending' });

    res.json({
      success: true,
      snapshotId,
      url: `/snapshot/${snapshotId}`,
      targetUrl: url,
      message: 'Snapshot queued! Our bot will visit and archive your page shortly.'
    });

    // Trigger Snapshot bot visit asynchronously - bot will fetch and save the page
    setTimeout(() => {
      visitAndSaveSnapshot(snapshotId, url).catch(err => {
        console.error(`Error creating snapshot ${snapshotId}:`, err.message);
        snapshotStatuses.set(snapshotId, { status: 'failed', error: err.message });
      });
    }, 2000);    
  } catch (error) {
    console.error('Error creating snapshot:', error);
    res.status(500).json({ error: 'Failed to create snapshot' });
  }
});

// View snapshot
app.get('/snapshot/:id', async (req, res) => {
  const snapshotId = req.params.id;
  const snapshotPath = path.join(SNAPSHOTS_DIR, `${snapshotId}.html`);
  
  if (!fs.existsSync(snapshotPath)) {
    return res.status(404).send('Snapshot not found');
  }
  
  // Pre-load snapshot resources for better performance
  await preloadSnapshotResources(snapshotId);
  
  res.sendFile(snapshotPath);
});

// Snapshot status endpoint (used by frontend polling)
app.get('/api/snapshot/:id/status', (req, res) => {
  const { id } = req.params;

  if (!/^[a-f0-9]{16}$/.test(id)) {
    return res.status(400).json({ error: 'Invalid snapshot ID' });
  }

  const status = snapshotStatuses.get(id);
  if (!status) {
    return res.status(404).json({ error: 'Snapshot not found' });
  }

  res.json(status);
});

// Helper function to download a file from URL
async function downloadFile(url, savePath) {
  return new Promise((resolve, reject) => {
    const protocol = url.startsWith('https') ? https : http;
    
    protocol.get(url, (response) => {
      if (response.statusCode !== 200) {
        reject(new Error(`Failed to download: ${response.statusCode}`));
        return;
      }
      
      const fileStream = fs.createWriteStream(savePath);
      response.pipe(fileStream);
      
      fileStream.on('finish', () => {
        fileStream.close();
        resolve();
      });
      
      fileStream.on('error', (err) => {
        fs.unlink(savePath, () => {});
        reject(err);
      });
    }).on('error', reject);
  });
}

// Extract resource URLs from HTML link tags
function extractResourceUrls(html, baseUrl) {
  const resources = [];
  
  // Extract all <link> tags with href attribute
  const linkRegex = /<link[^>]+href=["']([^"']+)["'][^>]*>/gi;
  let match;
  while ((match = linkRegex.exec(html)) !== null) {
    try {
      // Resolve relative URLs against base
      const absoluteUrl = new URL(match[1], baseUrl).toString();
      resources.push(absoluteUrl);
    } catch (e) {
      // If URL parsing fails, try the original
      resources.push(match[1]);
    }
  }
  
  return resources;
}

// Sanitize HTML content
function sanitizeHtmlContent(html) {
  return sanitizeHtml(html, {
    allowedTags: sanitizeHtml.defaults.allowedTags.concat(['link', 'meta']),
    allowedAttributes: {
      ...sanitizeHtml.defaults.allowedAttributes,
      link: ['rel', 'href', 'as', 'type', 'crossorigin'],
      meta: ['name', 'content', 'charset', 'http-equiv']
    },
    allowedSchemes: ['http', 'https', 'mailto', 'tel'],
    allowProtocolRelative: false
  });
}

// Archive resources in background
async function archiveResources(htmlContent, targetUrl) {
  console.log(`Extracting archive resources from page...`);
  const resourceUrls = extractResourceUrls(htmlContent, targetUrl);
  
  console.log(`Found ${resourceUrls.length} resources to archive`);
  
  for (const resourceUrl of resourceUrls) {
    try {
      console.log(`Archiving resource: ${resourceUrl}`);
      
      // Parse the URL
      const urlObj = new URL(resourceUrl);
      let filename = path.basename(urlObj.pathname);
      
      // Sanitize filename
      filename = filename.replace(/[^a-zA-Z0-9._-]/g, '_');
      
      if (!filename || filename === '_') {
        filename = 'resource_' + crypto.randomBytes(4).toString('hex');
      }
      
      const savePath = path.join(SNAPSHOTS_DIR, filename);
      
      console.log(`Saving to: ${savePath}`);
      
      // Download the resource
      await downloadFile(resourceUrl, savePath);
      console.log(`Resource archived: ${filename}`);
      
    } catch (err) {
      console.error(`Failed to archive resource ${resourceUrl}:`, err.message);
    }
  }
  
  console.log(`Finished archiving resources`);
}

// Snapshot bot visits URL and saves snapshot
async function visitAndSaveSnapshot(snapshotId, targetUrl) {
  console.log(`Snapshot bot fetching: ${targetUrl}`);

  const browser = await puppeteer.launch({
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-features=HttpsFirstBalancedModeAutoEnable'
    ]
  });

  try {
    const page = await browser.newPage();

    console.log(`Navigating to: ${targetUrl}`);

    // Use faster wait condition and longer timeout
    await page.goto(targetUrl, {
      waitUntil: 'domcontentloaded',
      timeout: 30_000
    });

    // Much shorter wait - just let DOM settle
    await new Promise(resolve => setTimeout(resolve, 500));

    console.log(`Page loaded, capturing snapshot...`);

    const htmlContent = await page.content();

    const snapshotPath = path.join(SNAPSHOTS_DIR, `${snapshotId}.html`);
    await fs.promises.writeFile(snapshotPath, sanitizeHtmlContent(htmlContent));

    console.log(`Snapshot saved: ${snapshotId}`);

    // Archive resources asynchronously in background - don't block
    setImmediate(() => {
      archiveResources(htmlContent, targetUrl)
        .then(() => {
          snapshotStatuses.set(snapshotId, { status: 'complete' });
        })
        .catch(err => {
          console.error('Background resource archiving error:', err.message);
      });
    });

    console.log(`Snapshot bot finished processing: ${snapshotId}`);
  } catch (err) {
    console.error('Error in Snapshot bot:', err);
  } finally {
    await browser.close();
  }
}

// Pre-load snapshot resources for faster rendering
// I dont know what resources there are, lets just use AI to write this
async function preloadSnapshotResources() {
  try {
    const entries = fs.readdirSync(SNAPSHOTS_DIR, { withFileTypes: true });

    for (const entry of entries) {
      if (!entry.isFile()) continue;

      const filePath = path.join(SNAPSHOTS_DIR, entry.name);      
      // Load optimization helpers
      if (path.extname(entry.name) === '.js') {
        try {
          require(filePath);
        } catch (err) {
          // Skip invalid helpers
        }
      }
    }
  } catch (error) {
    // Ignore resource loading errors
  }
}

app.get('/api/snapshots', (req, res) => {
  try {
    const files = fs.readdirSync(SNAPSHOTS_DIR);
    const snapshots = files
      .filter(f => f.endsWith('.html'))
      .map(f => ({
        id: f.replace('.html', ''),
        name: f
      }));
    res.json({ snapshots });
  } catch (error) {
    res.status(500).json({ error: 'Failed to list snapshots' });
  }
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`WayWayBack Machine running on http://0.0.0.0:${PORT}`);
  console.log(`Snapshots directory: ${SNAPSHOTS_DIR}`);
});