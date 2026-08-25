const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const webpanelDir = path.join(__dirname, '../webpanel');

// Mock Config matching ConfigOnofre structure
const initialConfig = {
  nodeId: "test-node",
  chipId: "123456",
  mcu: "ESP32",
  firmwareVersion: "9.199",
  wifiSSID: "Home_WiFi",
  wifiSecret: "hide_password",
  dhcp: true,
  wifiIp: "192.168.1.100",
  wifiMask: "255.255.255.0",
  wifiGw: "192.168.1.254",
  mqttIpDns: "192.168.1.10",
  mqttPort: 1883,
  mqttUsername: "admin",
  mqttPassword: "hide_password",
  outInPins: [4, 5, 12, 13, 14, 25, 26, 27, 32, 33],
  inPins: [17, 34, 35],
  features: [
    {
      group: "ACTUATOR",
      driver: "LIGHT_PUSH",
      id: "light1",
      name: "Cozinha",
      typeControl: 0,
      state: 0,
      inputs: [12],
      outputs: [13]
    },
    {
      group: "ACTUATOR",
      driver: "GARDEN_VALVE",
      id: "valve1",
      name: "Bico Central",
      typeControl: 0,
      state: 0,
      inputs: [],
      outputs: [27]
    }
  ]
};

let config = JSON.parse(JSON.stringify(initialConfig));
let requestsLog = [];

app.use((req, res, next) => {
  if (req.path !== '/config' || req.method !== 'GET') {
    requestsLog.push({
      method: req.method,
      path: req.path,
      body: req.body,
      query: req.query
    });
  }
  next();
});

// Serve index.html with replaced version tag
app.get('/', (req, res) => {
  const htmlPath = path.join(webpanelDir, 'index.html');
  if (fs.existsSync(htmlPath)) {
    let html = fs.readFileSync(htmlPath, 'utf8');
    html = html.replace(/__ASSET_VERSION__/g, '9.199');
    res.type('html').send(html);
  } else {
    res.status(404).send('Not Found');
  }
});

// Static assets (css, js)
app.use(express.static(webpanelDir));

// REST Endpoints
app.get('/config', (req, res) => {
  res.json(config);
});

app.post('/config', (req, res) => {
  config = { ...config, ...req.body };
  res.json({ status: "success", config });
});

app.get('/aquadance', (req, res) => {
  res.json({
    activeShow: 0,
    running: false,
    shows: [
      {
        id: 1,
        name: "Dança das Águas",
        stepDurationMs: 300,
        repeat: true,
        stepsCount: 32,
        nodes: [
          { fixtureId: "valve1", fixtureType: 0, x: 50, y: 50 }
        ],
        tracks: [
          { fixtureId: "valve1", trackType: 0, steps: [1,0,1,0,1,0,1,0] }
        ]
      }
    ]
  });
});

app.post('/aquadance', (req, res) => {
  res.json({ status: "saved" });
});

app.post(['/aquadance/run', '/aquadance-run'], (req, res) => {
  res.json({ status: "started" });
});

app.post(['/aquadance/stop', '/aquadance-stop'], (req, res) => {
  res.json({ status: "stopped" });
});

app.all('/reboot', (req, res) => {
  res.json({ status: "rebooting" });
});

app.get('/test/logs', (req, res) => {
  res.json(requestsLog);
});

app.post('/test/reset-all', (req, res) => {
  config = JSON.parse(JSON.stringify(initialConfig));
  requestsLog = [];
  res.json({ status: "all_reset" });
});

let server;
function startServer(port = 3000) {
  return new Promise((resolve) => {
    server = app.listen(port, () => {
      console.log(`[MOCK] ESP WebServer running at http://localhost:${port}`);
      resolve(`http://localhost:${port}`);
    });
  });
}

function stopServer() {
  if (server) {
    server.close();
    console.log('[MOCK] Server stopped.');
  }
}

module.exports = { startServer, stopServer };
